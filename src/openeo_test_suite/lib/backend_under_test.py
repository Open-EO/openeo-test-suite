"""

Pytest plugin to allow parameterizing tests over the available collections and processes
of the openEO backend under test.

Originally this was approximated through fixtures, but fixtures are evaluated at test execution time,
not test collection time, making it practically impossible to implement proper parametrization.


"""
import abc
import functools
import logging
import os
from typing import List, Union

import openeo
import pytest

_log = logging.getLogger(__name__)


class _BackendUnderTest(metaclass=abc.ABCMeta):
    """Abstract base class for back-end under test."""

    @abc.abstractmethod
    def list_collection_ids(self) -> List[str]:
        """List available collections."""
        ...

    @abc.abstractmethod
    def list_process_ids(self) -> List[str]:
        """List available processes."""
        ...


class HttpBackend(_BackendUnderTest):
    """Back-end under test that uses the openEO HTTP API."""

    def __init__(self, connection: openeo.Connection):
        self.connection = connection

    def list_collection_ids(self) -> List[str]:
        return [c["id"] for c in self.connection.list_collections()]

    def list_process_ids(self) -> List[str]:
        return [p["id"] for p in self.connection.list_processes()]


class NoBackend(_BackendUnderTest):
    """No backend under test, just to get basic test suite setup working."""

    def list_collection_ids(self) -> List[str]:
        return []

    def list_process_ids(self) -> List[str]:
        return []


def get_backend_url(config: pytest.Config, required: bool = False) -> Union[str, None]:
    """
    Get openEO backend URL from command line options or environment variable.

    :param config: pytest config object, e.g. `request.config` from the `request` fixture
    :param required: Whether the backend URL must be set or can be None.
        It's recommended to only require it from within tests and fixtures.
        In more generic cases it must be considered optional,
        so that the test suite can be constructed/run even when no backend is specified.
    """
    url = config.getoption(
        "--openeo-backend-url", default=os.environ.get("OPENEO_BACKEND_URL")
    )

    if required and not url:
        raise ValueError(
            "No openEO backend URL found."
            " Specify it using the `--openeo-backend-url` command line option (short form `-U`),"
            " or through the 'OPENEO_BACKEND_URL' environment variable"
        )

    if isinstance(url, str) and "://" not in url:
        url = f"https://{url}"

    return url


# Internal singleton, pointing to backend under test,
# setup happens in `pytest_configure` hook
_backend_under_test: Union[None, _BackendUnderTest] = None


def pytest_addoption(parser):
    """Implementation of `pytest_addoption` hook."""
    parser.addoption(
        "-U",
        "--openeo-backend-url",
        action="store",
        default=None,
        help="The openEO backend URL to connect to.",
    )


def pytest_configure(config):
    """Implementation of `pytest_configure` hook."""
    global _backend_under_test
    assert _backend_under_test is None
    backend_url = get_backend_url(config)
    if backend_url is None:
        _backend_under_test = NoBackend()
    else:
        connection = openeo.connect(url=backend_url, auto_validate=False)
        _backend_under_test = HttpBackend(connection=connection)


def _get_backend_under_test() -> _BackendUnderTest:
    global _backend_under_test
    assert isinstance(_backend_under_test, _BackendUnderTest)
    return _backend_under_test


@functools.lru_cache
def get_collection_ids() -> List[str]:
    return _get_backend_under_test().list_collection_ids()


@functools.lru_cache
def get_process_ids() -> List[str]:
    return _get_backend_under_test().list_process_ids()
