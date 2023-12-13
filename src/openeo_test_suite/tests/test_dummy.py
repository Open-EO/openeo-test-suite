from urllib.parse import urlparse


def test_backend_url(backend_url):
    assert isinstance(backend_url, str) or backend_url is None
    if backend_url is not None:
        result = urlparse(backend_url)
        assert result.scheme in ["http", "https"]
        assert len(result.netloc) > 0
