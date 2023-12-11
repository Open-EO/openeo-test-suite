import os

import openeo
import pytest


@pytest.fixture
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return True


@pytest.fixture
def bounding_box_small(
    west=10.47, east=10.48, south=46.12, north=46.13, crs="EPSG:4326"
) -> dict:
    spatial_extent = {
        "west": west,
        "east": east,
        "south": south,
        "north": north,
        "crs": crs,
    }
    return spatial_extent


@pytest.fixture
def temporal_interval(interval=["2019-06-01", "2019-07-01"]):
    return interval


@pytest.fixture
def temporal_interval_one_day(interval=["2019-06-03", "2019-06-05"]):
    return interval


@pytest.fixture
def s2_stac_url(
    url="https://planetarycomputer.microsoft.com/api/stac/v1/collections/sentinel-2-l2a",
):
    return url


@pytest.fixture
def t_dim(t_dim="time"):
    return t_dim


@pytest.fixture
def b_dim(b_dim="band"):
    return b_dim
