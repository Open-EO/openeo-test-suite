import importlib
import inspect

import dask
from openeo_pg_parser_networkx import OpenEOProcessGraph, ProcessRegistry
from openeo_pg_parser_networkx.pg_schema import BoundingBox
from openeo_pg_parser_networkx.process_registry import Process
from openeo_processes_dask.process_implementations.core import process

from openeo_test_suite.lib.process_runner.base import ProcessTestRunner
from openeo_test_suite.lib.process_runner.util import (
    datacube_to_xarray,
    numpy_to_native,
    xarray_to_datacube,
)


def create_process_registry():
    process_registry = ProcessRegistry(wrap_funcs=[process])

    processes_from_module = [
        func
        for _, func in inspect.getmembers(
            importlib.import_module("openeo_processes_dask.process_implementations"),
            inspect.isfunction,
        )
    ]

    # not sure why this is needed
    import openeo_processes_dask.process_implementations.math

    processes_from_module.append(openeo_processes_dask.process_implementations.math.e)

    specs_module = importlib.import_module("openeo_processes_dask.specs")
    specs = {
        func.__name__: getattr(specs_module, func.__name__)
        for func in processes_from_module
    }

    for func in processes_from_module:
        process_registry[func.__name__] = Process(
            spec=specs[func.__name__], implementation=func
        )

    return process_registry


registry = create_process_registry()


class Dask(ProcessTestRunner):
    def list_processes(self):
        return map(lambda process: process.spec, registry.values())

    def describe_process(self, process_id):
        return registry[process_id].spec

    def execute(self, id, arguments):
        callable = registry[id].implementation
        return callable(**arguments)

    def encode_process_graph(
        self, process, parent_process_id=None, parent_parameter=None
    ):
        parsed = OpenEOProcessGraph(pg_data=process)
        return parsed.to_callable(process_registry=registry)

    def encode_datacube(self, data):
        return datacube_to_xarray(data)

    def encode_data(self, data):
        if (
            isinstance(data, dict)
            and "south" in data
            and "west" in data
            and "north" in data
            and "east" in data
        ):
            try:
                return BoundingBox(**data)
            except Exception as e:
                raise ValueError("Failed to encode bounding box") from e

        return data

    def decode_data(self, data, expected):
        if isinstance(data, dask.array.core.Array):
            data = data.compute()

        data = numpy_to_native(data, expected)
        data = xarray_to_datacube(data)

        return data

    def get_nodata_value(self):
        return float("nan")
