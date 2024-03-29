# TODO rename this module (`test_example.py` was originally just meant as an example)

import logging
import math
import warnings
from pathlib import Path
from typing import List, Tuple, Union

import json5
import pytest
from deepdiff import DeepDiff

from openeo_test_suite.lib.process_runner.base import ProcessTestRunner
from openeo_test_suite.lib.process_runner.util import isostr_to_datetime
from openeo_test_suite.lib.process_selection import get_selected_processes

_log = logging.getLogger(__name__)


def get_examples() -> List[Tuple[str, dict, Path, str, bool]]:
    """Collect process examples/tests from examples root folder containing JSON5 files."""
    return [
        (
            process.process_id,
            test,
            process.path,
            test.get("level", process.level),
            test.get("experimental", process.experimental),
        )
        for process in get_selected_processes()
        for test in process.tests
    ]


@pytest.mark.parametrize(
    ["process_id", "example", "file", "level", "experimental"], get_examples()
)
def test_process(
    connection,
    process_id,
    example,
    file,
    level,
    experimental,
    skipper,
):
    # Check whether the process (and additional extra required ones, if any) is supported on the backend
    skipper.skip_if_unsupported_process([process_id] + example.get("required", []))

    # prepare the arguments from test JSON encoding to internal backend representations
    # or skip if not supported by the test runner
    try:
        arguments = _prepare_arguments(
            arguments=example["arguments"],
            process_id=process_id,
            connection=connection,
            file=file,
        )
    except NotImplementedError as e:
        pytest.skip(str(e))

    throws = bool(example.get("throws"))
    returns = "returns" in example

    # execute the process
    try:
        result = connection.execute(process_id, arguments)
    except Exception as e:
        result = e

    # check the process results / behavior
    if throws and returns:
        if isinstance(result, Exception):
            check_exception(example, result)
        else:
            check_return_value(example, result, connection, file)
    elif throws:
        check_exception(example, result)
    elif returns:
        check_return_value(example, result, connection, file)
    else:
        pytest.skip(
            f"Test for process {process_id} doesn't provide an expected result for arguments: {example['arguments']}"
        )


def _prepare_arguments(
    arguments: dict, process_id: str, connection: ProcessTestRunner, file: Path
) -> dict:
    return {
        k: _prepare_argument(
            arg=v, process_id=process_id, name=k, connection=connection, file=file
        )
        for k, v in arguments.items()
    }


def _prepare_argument(
    arg: Union[dict, str, int, float],
    process_id: str,
    name: str,
    connection: ProcessTestRunner,
    file: Path,
):
    # handle external references to files
    if isinstance(arg, dict) and "$ref" in arg:
        arg = _load_ref(arg["$ref"], file)

    # handle custom types of data
    if isinstance(arg, dict):
        if "type" in arg:
            # labeled arrays
            if arg["type"] == "labeled-array":
                arg = connection.encode_labeled_array(arg)
            # datacubes
            elif arg["type"] == "datacube":
                arg = connection.encode_datacube(arg)
            # nodata-values
            elif arg["type"] == "nodata":
                arg = connection.get_nodata_value()
            else:
                # TODO: raise NotImplementedError?
                _log.warning(f"Unhandled argument type: {arg}")
        elif "process_graph" in arg:
            arg = connection.encode_process_graph(
                process=arg, parent_process_id=process_id, parent_parameter=name
            )
        else:
            arg = {
                k: _prepare_argument(
                    arg=v,
                    process_id=process_id,
                    name=name,
                    connection=connection,
                    file=file,
                )
                for k, v in arg.items()
            }

    elif isinstance(arg, list):
        arg = [
            _prepare_argument(
                arg=a,
                process_id=process_id,
                name=name,
                connection=connection,
                file=file,
            )
            for a in arg
        ]

    arg = connection.encode_data(arg)

    if connection.is_json_only():
        check_non_json_values(arg)

    return arg


def _prepare_results(connection: ProcessTestRunner, file: Path, example, result=None):
    # go through the example and result recursively and convert datetimes to iso strings
    # could be used for more conversions in the future...

    if isinstance(example, dict):
        # handle external references to files
        if isinstance(example, dict) and "$ref" in example:
            example = _load_ref(example["$ref"], file)

        if "type" in example:
            if example["type"] == "datetime":
                example = isostr_to_datetime(example["value"])
                try:
                    result = isostr_to_datetime(result)
                except Exception:
                    pass
            elif example["type"] == "nodata":
                example = connection.get_nodata_value()
        else:
            # TODO: avoid in-place dict mutation
            for key in example:
                if key not in result:
                    (example[key], _) = _prepare_results(
                        connection=connection, file=file, example=example[key]
                    )
                else:
                    (example[key], result[key]) = _prepare_results(
                        connection=connection,
                        file=file,
                        example=example[key],
                        result=result[key],
                    )

    elif isinstance(example, list):
        # TODO: avoid in-place list mutation
        for i in range(len(example)):
            if i >= len(result):
                (example[i], _) = _prepare_results(
                    connection=connection, file=file, example=example[i]
                )
            else:
                (example[i], result[i]) = _prepare_results(
                    connection=connection,
                    file=file,
                    example=example[i],
                    result=result[i],
                )

    return (example, result)


def _load_ref(ref: str, file: Path):
    try:
        path = file.parent / ref
        if ref.endswith(".json") or ref.endswith(".json5") or ref.endswith(".geojson"):
            with open(path) as f:
                return json5.load(f)
        elif ref.endswith(".txt") or ref.endswith(".wkt2"):
            with open(path) as f:
                return f.read()
        else:
            raise NotImplementedError(f"Unhandled external reference {ref}.")
    except Exception as e:
        # TODO: is this try-except actually useful?
        raise RuntimeError(f"Failed to load external reference {ref}") from e


def check_non_json_values(value):
    # TODO: shouldn't this check be an aspect of Http(ProcessTestRunner)?
    if isinstance(value, float):
        if math.isnan(value):
            raise ValueError("HTTP JSON APIs don't support NaN values")
        elif math.isinf(value):
            raise ValueError("HTTP JSON APIs don't support infinity values")
    elif isinstance(value, dict):
        for v in value.values():
            check_non_json_values(v)
    elif isinstance(value, list):
        for item in value:
            check_non_json_values(item)


def check_exception(example, result):
    assert isinstance(result, Exception), f"Expected an exception, but got {result}"
    if isinstance(example["throws"], str):
        # todo: we should assert here and remove the warning, but right now tooling doesn't really implement this
        # assert result.__class__.__name__ == example["throws"]
        if result.__class__.__name__ != example["throws"]:
            warnings.warn(f"Expected exception {example['throws']} but got {result!r}")


def check_return_value(example, result, connection, file):
    assert not isinstance(result, Exception), f"Unexpected exception: {result}"

    # handle custom types of data
    result = connection.decode_data(result, example["returns"])

    # decode special types (currently mostly datetimes and nodata)
    (example["returns"], result) = _prepare_results(
        connection=connection, file=file, example=example["returns"], result=result
    )

    delta = example.get("delta", 0.0000000001)

    if isinstance(example["returns"], dict):
        assert isinstance(result, dict), f"Expected a dict but got {type(result)}"
        exclude_regex_paths = []
        exclude_paths = []
        ignore_order_func = None
        if "type" in example["returns"] and example["returns"]["type"] == "datacube":
            # todo: non-standardized
            exclude_regex_paths.append(
                r"root\['dimensions'\]\[[^\]]+\]\['reference_system'\]"
            )
            # todo: non-standardized
            exclude_paths.append("root['nodata']")
            # ignore data if operation is not changing data
            if example["returns"]["data"] is None:
                exclude_paths.append("root['data']")

        diff = DeepDiff(
            example["returns"],
            result,
            math_epsilon=delta,
            ignore_numeric_type_changes=True,
            ignore_nan_inequality=True,
            exclude_paths=exclude_paths,
            exclude_regex_paths=exclude_regex_paths,
            ignore_order_func=ignore_order_func,
        )
        assert {} == diff, f"Differences: {diff!s}"
    elif isinstance(example["returns"], list):
        assert isinstance(result, list), f"Expected a list but got {type(result)}"
        diff = DeepDiff(
            example["returns"],
            result,
            math_epsilon=delta,
            ignore_numeric_type_changes=True,
            ignore_nan_inequality=True,
        )
        assert {} == diff, f"Differences: {diff!s}"
    elif isinstance(example["returns"], float) and math.isnan(example["returns"]):
        assert isinstance(result, float) and math.isnan(
            result
        ), f"Got {result} instead of NaN"
    elif isinstance(example["returns"], float) or isinstance(example["returns"], int):
        msg = f"Expected a numerical result but got {result} of type {type(result)}"
        assert isinstance(result, float) or isinstance(result, int), msg
        assert not math.isnan(result), "Got unexpected NaN as result"
        # handle numerical data with a delta
        assert result == pytest.approx(example["returns"], rel=delta)
    else:
        msg = f"Expected {example['returns']} but got {result}"
        assert result == example["returns"], msg
