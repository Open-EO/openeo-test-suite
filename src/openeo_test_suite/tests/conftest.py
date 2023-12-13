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
    parser.addoption(
        "--process-levels",
        action="store",
        default="",
        help="The openEO process profiles you want to test against, e.g. 'L1,L2,L2A'. Mutually exclusive with --processes.",
    )
    parser.addoption(
        "--processes",
        action="store",
        default="",
        help="The openEO processes you want to test against, e.g. 'apply,reduce_dimension'. Mutually exclusive with --process-levels.",
    )
    parser.addoption(
        "--runner",
        action="store",
        default=None,
        help="A specific test runner to use for individual process tests. If not provided, uses a default HTTP API runner.",
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
        url = None

    if isinstance(url, str) and "://" not in url:
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
    if not backend_url:
        raise RuntimeError(
            "No openEO backend URL found. Specify it using the `--openeo-backend-url` command line option or through the 'OPENEO_BACKEND_URL' environment variable"
        )

    con = openeo.connect(backend_url, auto_validate=False)

    if auto_authenticate:
        auth_method = os.environ.get("OPENEO_AUTH_METHOD")

        if auth_method == "none":
            pass
        elif auth_method == "basic":
            con.authenticate_basic(
                username=os.environ.get("OPENEO_AUTH_BASIC_USERNAME"),
                password=os.environ.get("OPENEO_AUTH_BASIC_PASSWORD"),
            )
        else:
            # Temporarily disable output capturing, to make sure that OIDC device code instructions (if any) are visible to the user.
            with capfd.disabled():
                # Note: this generic `authenticate_oidc()` call allows both:
                # - device code/refresh token based authentication for manual test suite runs
                # - client credentials auth through env vars for automated/Jenkins CI runs
                #
                # See https://open-eo.github.io/openeo-python-client/auth.html#oidc-authentication-dynamic-method-selection
                con.authenticate_oidc()

    return con
