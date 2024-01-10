import logging
from typing import List

import openeo
import pytest

_log = logging.getLogger(__name__)


class Skipper:
    """
    Helper class to compactly skip tests for based on
    backend capabilities and configuration.
    """

    def __init__(self, connection: openeo.Connection, process_levels: List[str]):
        self._connection = connection
        self._process_levels = process_levels

    def _get_output_formats(self) -> set:
        formats = set(
            f.lower() for f in self._connection.list_file_formats()["output"].keys()
        )
        _log.info("Detected output formats: %s", formats)
        return formats

    def skip_if_no_netcdf_support(self):
        output_formats = self._get_output_formats()
        if not output_formats.intersection({"netcdf", "nc"}):
            pytest.skip("NetCDF not supported as output file format")

    def skip_if_no_geotiff_support(self):
        output_formats = self._get_output_formats()
        if not output_formats.intersection({"geotiff", "gtiff"}):
            pytest.skip("GeoTIFF not supported as output file format")

    def skip_if_unmatching_process_level(self, level: str):
        """Skip test if "process_levels" are set and do not match the given level."""
        if len(self._process_levels) > 0 and level not in self._process_levels:
            pytest.skip(
                f"Skipping {level} test because the specified levels are: {self._process_levels}"
            )
