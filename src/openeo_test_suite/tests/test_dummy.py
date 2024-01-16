from urllib.parse import urlparse

from openeo_test_suite.lib.backend_under_test import get_backend_url


def test_dummy():
    """
    This is a dummy test for verifying the basic test suite setup
    without triggering real openEO connections or processing.
    """
    assert True


def test_backend_url(request):
    backend_url = get_backend_url(request.config, required=False)
    if isinstance(backend_url, str):
        result = urlparse(backend_url)
        assert result.scheme in ["http", "https"]
        assert len(result.netloc) > 0
    elif backend_url is None:
        pass
    else:
        raise ValueError(backend_url)
