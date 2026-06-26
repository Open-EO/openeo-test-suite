import json
import urllib

import openeo
import pystac_client
import pytest

from openeo_test_suite.lib.workflows.parameters import (
    bounding_box_32632,
    bounding_box_32632_10x10,
    temporal_interval,
    temporal_interval_one_day,
)


@pytest.fixture
def s2_collection(request) -> str:
    """
    Fixture to provide the data collection to test against.
    If we provide a string, it will be interpreted as openEO Collection.
    If it's an URL, it's interpreted as STAC Collection.
    """
    collection = request.config.getoption("--s2-collection")
    if not collection:
        raise RuntimeError(
            "No S2 test collection found. Specify it using the `--s2-collection` command line option."
        )
    return collection


@pytest.fixture(scope="module")
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return True


@pytest.fixture
def cube_one_day_red(
    connection,
    s2_collection,
    skipper,
) -> openeo.DataCube:
    params = {
        "spatial_extent": bounding_box_32632,
        "temporal_extent": temporal_interval_one_day,
        "bands": ["B04"],
    }
    if "http" in s2_collection:
        skipper.skip_if_unsupported_process(["load_stac", "save_result"])
        cube = connection.load_stac(s2_collection, **params)
    else:
        skipper.skip_if_unsupported_process(["load_collection", "save_result"])
        cube = connection.load_collection(s2_collection, **params)
    return cube


@pytest.fixture
def cube_one_day_red_nir(
    connection,
    s2_collection,
    skipper,
) -> openeo.DataCube:
    params = {
        "spatial_extent": bounding_box_32632,
        "temporal_extent": temporal_interval_one_day,
        "bands": ["B04", "B08"],
    }
    if "http" in s2_collection:
        skipper.skip_if_unsupported_process(["load_stac", "save_result"])
        cube = connection.load_stac(s2_collection, **params)
    else:
        skipper.skip_if_unsupported_process(["load_collection", "save_result"])
        cube = connection.load_collection(s2_collection, **params)
    return cube


@pytest.fixture
def cube_red_nir(
    connection,
    s2_collection,
    skipper,
) -> openeo.DataCube:
    params = {
        "spatial_extent": bounding_box_32632,
        "temporal_extent": temporal_interval,
        "bands": ["B04", "B08"],
    }
    if "http" in s2_collection:
        skipper.skip_if_unsupported_process(["load_stac", "save_result"])
        cube = connection.load_stac(s2_collection, **params)
    else:
        skipper.skip_if_unsupported_process(["load_collection", "save_result"])
        cube = connection.load_collection(s2_collection, **params)
    return cube


@pytest.fixture
def cube_red_10x10(
    connection,
    s2_collection,
    skipper,
) -> openeo.DataCube:
    params = {
        "spatial_extent": bounding_box_32632_10x10,
        "temporal_extent": temporal_interval_one_day,
        "bands": ["B04"],
    }
    if "http" in s2_collection:
        skipper.skip_if_unsupported_process(["load_stac", "save_result"])
        cube = connection.load_stac(s2_collection, **params)
    else:
        skipper.skip_if_unsupported_process(["load_collection", "save_result"])
        cube = connection.load_collection(s2_collection, **params)
    return cube


@pytest.fixture
def collection_dims(
    connection,
    s2_collection,
):
    if "/" in s2_collection:
        # I consider it as a STAC url
        parsed_url = urllib.parse.urlparse(s2_collection)
        if not bool(parsed_url.scheme):
            parsed_url = parsed_url._replace(**{"scheme": "https"})
        s2_collection_url = parsed_url.geturl()
        stac_api = pystac_client.stac_api_io.StacApiIO()
        stac_dict = json.loads(stac_api.read_text(s2_collection_url))
    else:
        # I consider it as an openEO Collection
        stac_dict = dict(connection.describe_collection(s2_collection))
    collection_dims = dict(b_dim="bands", t_dim="t", x_dim="x", y_dim="y", z_dim="z")
    if "cube:dimensions" in stac_dict:
        for dim in stac_dict["cube:dimensions"]:
            if stac_dict["cube:dimensions"][dim]["type"] == "bands":
                collection_dims["b_dim"] = dim
            if stac_dict["cube:dimensions"][dim]["type"] == "temporal":
                collection_dims["t_dim"] = dim
            if stac_dict["cube:dimensions"][dim]["type"] == "spatial":
                if stac_dict["cube:dimensions"][dim]["axis"] == "x":
                    collection_dims["x_dim"] = dim
                if stac_dict["cube:dimensions"][dim]["axis"] == "y":
                    collection_dims["y_dim"] = dim
                if stac_dict["cube:dimensions"][dim]["axis"] == "z":
                    collection_dims["z_dim"] = dim
    return collection_dims
