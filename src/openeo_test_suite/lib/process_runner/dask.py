import importlib
import inspect

from openeo_pg_parser_networkx import OpenEOProcessGraph, ProcessRegistry
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

    def execute(self, process):
        parsed = OpenEOProcessGraph(pg_data=process)
        callable = parsed.to_callable(process_registry=registry)
        return callable()

    def encode_datacube(self, data):
        return datacube_to_xarray(data)

    def decode_data(self, data):
        data = numpy_to_native(data)
        data = xarray_to_datacube(data)
        return data
