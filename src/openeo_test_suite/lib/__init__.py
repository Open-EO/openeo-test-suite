import pytest

# Register some helper modules for assert rewriting to improve test reporting
pytest.register_assert_rewrite(
    "openeo_test_suite.lib.collection_metadata",
)
