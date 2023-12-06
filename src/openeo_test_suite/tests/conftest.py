import logging
import os

import openeo
import pytest

_log = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--openeo-backend-url",
        action="store",
        default=None,
        help="The openEO backend URL to connect to.",
    )


@pytest.fixture(scope="session")
def backend_url(request) -> str:
    """
    Fixture to get the desired openEO back-end URL to test against.
    """
    # TODO: also support getting it from a config file?
    if request.config.getoption("--openeo-backend-url"):
        url = request.config.getoption("--openeo-backend-url")
    elif "OPENEO_BACKEND_URL" in os.environ:
        url = os.environ["OPENEO_BACKEND_URL"]
    else:
        raise RuntimeError(
            "No openEO backend URL found. Specify it using the `--openeo-backend-url` command line option or through the 'OPENEO_BACKEND_URL' environment variable"
        )

    if "://" not in url:
        url = f"https://{url}"

    _log.info(f"Using openEO back-end URL {url!r}")

    return url


@pytest.fixture
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return False


@pytest.fixture
def connection(backend_url: str, auto_authenticate: bool, capfd) -> openeo.Connection:
    con = openeo.connect(backend_url, auto_validate=False)

    if auto_authenticate:
        # Temporarily disable output capturing, to make sure that OIDC device code instructions (if any) are visible to the user.
        with capfd.disabled():
            # Note: this generic `authenticate_oidc()` call allows both:
            # - device code/refresh token based authentication for manual test suite runs
            # - client credentials auth through env vars for automated/Jenkins CI runs
            #
            # See https://open-eo.github.io/openeo-python-client/auth.html#oidc-authentication-dynamic-method-selection
            try: # TODO: probably there's a more elegant solution to have authenticate_basic as well?
                con.authenticate_oidc()
            except Exception as e:
                con.authenticate_basic()

    return con
