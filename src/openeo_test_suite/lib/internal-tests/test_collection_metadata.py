import pytest

from openeo_test_suite.lib.collection_metadata import OpeneoApiCollectionTests


@pytest.mark.parametrize(
    ["stac_version", "extra_stac_extensions", "expect_success"],
    [
        ("0.9.0", [], True),
        ("1.0.0-beta.1", [], False),
        ("1.0.0-beta.1", ["collection-assets"], True),
        ("1.0.0-beta.2", [], False),
        ("1.0.0-beta.2", ["collection-assets"], True),
        ("1.0.0-rc.1", [], True),
        ("1.0.0", [], True),
    ],
)
def test_collection_assets(stac_version, extra_stac_extensions, expect_success):
    stac_extensions = [
        "https://stac-extensions.github.io/datacube/v2.2.0/schema.json"
    ] + extra_stac_extensions
    collection = {
        "stac_version": stac_version,
        "stac_extensions": stac_extensions,
        "id": "S2",
        "cube:dimensions": {},
        "summaries": {},
        "assets": {},
    }
    try:
        OpeneoApiCollectionTests(collection)
        success = True
    except AssertionError:
        success = False

    assert success == expect_success
