import openeo
import pytest

from openeo_test_suite.lib.skipping import extract_processes_from_process_graph


def test_extract_processes_from_process_graph_basic():
    pg = {"add35": {"process_id": "add", "arguments": {"x": 3, "y": 5}, "result": True}}
    assert extract_processes_from_process_graph(pg) == {"add"}


@pytest.fixture
def s2_cube() -> openeo.DataCube:
    return openeo.DataCube.load_collection(
        collection_id="S2", bands=["B02", "B03"], connection=None, fetch_metadata=False
    )


def test_extract_processes_from_process_graph_cube_simple(s2_cube):
    assert extract_processes_from_process_graph(s2_cube) == {"load_collection"}


def test_extract_processes_from_process_graph_cube_reduce_temporal(s2_cube):
    cube = s2_cube.reduce_temporal("mean")
    assert extract_processes_from_process_graph(cube) == {
        "load_collection",
        "reduce_dimension",
        "mean",
    }


def test_extract_processes_from_process_graph_cube_reduce_bands(s2_cube):
    b2 = s2_cube.band("B02")
    b3 = s2_cube.band("B03")
    cube = (b3 - b2) / (b3 + b2)
    assert extract_processes_from_process_graph(cube) == {
        "load_collection",
        "reduce_dimension",
        "array_element",
        "subtract",
        "add",
        "divide",
    }
