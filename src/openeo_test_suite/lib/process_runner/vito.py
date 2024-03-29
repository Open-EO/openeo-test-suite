from openeo_driver.ProcessGraphDeserializer import process_registry_2xx

from openeo_test_suite.lib.process_runner.base import ProcessTestRunner
from openeo_test_suite.lib.process_runner.util import (
    datacube_to_xarray,
    numpy_to_native,
    xarray_to_datacube,
)


class Vito(ProcessTestRunner):
    def list_processes(self):
        return process_registry_2xx.get_specs()

    def execute(self, id, arguments):
        fn = process_registry_2xx.get_function(id)
        return fn(arguments, env=None)

    def encode_datacube(self, data):
        return datacube_to_xarray(data)

    def decode_data(self, data, expected):
        data = numpy_to_native(data, expected)
        data = xarray_to_datacube(data)
        return data

    def get_nodata_value(self):
        return float("nan")
