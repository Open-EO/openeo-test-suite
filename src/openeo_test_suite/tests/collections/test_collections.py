import logging
import re

import pytest
from stac_validator import stac_validator

from openeo_test_suite.lib.backend_under_test import get_collection_ids
from openeo_test_suite.tests.collections.openeo_api_collection_tests import (
    OpeneoApiCollectionTests,
)

_log = logging.getLogger(__name__)


def validate_stac_dict(collection_dict: dict):
    stac = stac_validator.StacValidate()
    is_valid_stac = stac.validate_dict(collection_dict)
    if not is_valid_stac:
        raise ValueError(stac.message)


def test_get_collections(connection):
    """
    Check `GET /collections` response:
    1. The request returns a valid JSON, containing the collections and links lists.
    Both of them are mandatory, see here:
    https://api.openeo.org/#tag/EO-Data-Discovery/operation/list-collections
    2. The JSON document describing each Collection in the list
    is a valid STAC. For each invalid Collection it logs an informative error.
    """
    response = connection.get("/collections").json()
    assert "collections" in response
    assert "links" in response
    for coll in response["collections"]:
        validate_stac_dict(coll)


@pytest.mark.parametrize("collection_id", get_collection_ids())
def test_get_collections_collection_id(connection, collection_id):
    """
    Check `GET /collections/{collection_id}` response:
    Verify that the JSON document describing each Collection is a valid STAC.
    For each invalid Collection it logs an informative error.
    """
    resp = connection.get(f"/collections/{collection_id}").json()
    validate_stac_dict(resp)

    # Tests specifics for openEO API specs
    # TODO: avoid this OOP pattern.
    OpeneoApiCollectionTests(resp)


@pytest.mark.parametrize("collection_id", get_collection_ids())
def test_valid_collection_id(collection_id: str):
    assert re.match(r"^[\w\-.~/]+$", collection_id, flags=re.IGNORECASE)
