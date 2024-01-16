import argparse
import logging
import os
from distutils.util import strtobool
from typing import List

import openeo
import pytest

from openeo_test_suite.lib.backend_under_test import get_backend_url
from openeo_test_suite.lib.skipping import Skipper

_log = logging.getLogger(__name__)


def pytest_addoption(parser):
    parser.addoption(
        "--experimental",
        type=bool,
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Run tests for experimental functionality or not. By default the tests will be skipped.",
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
    parser.addoption(
        "--s2-collection",
        action="store",
        default=None,
        help="The data collection to test against. It can be either a Sentinel-2 STAC Collection or the name of an openEO Sentinel-2 Collection provided by the back-end.",
    )


@pytest.fixture(scope="session")
def skip_experimental(request) -> bool:
    """
    Fixture to determine whether experimental functionality should be tested or not.
    """
    # TODO: also support getting it from a config file?
    if request.config.getoption("--experimental"):
        skip = False
    elif "OPENEO_EXPERIMENTAL" in os.environ:
        skip = bool(strtobool(os.environ["OPENEO_EXPERIMENTAL"]))
    else:
        skip = True

    _log.info(f"Skip experimental functionality {skip!r}")

    return skip


@pytest.fixture(scope="session")
def process_levels(request) -> List[str]:
    """
    Fixture to get the desired openEO profiles levels.
    """
    levels_str = ""
    # TODO: also support getting it from a config file?
    if request.config.getoption("--process-levels"):
        levels_str = request.config.getoption("--process-levels")
    elif "OPENEO_PROCESS_LEVELS" in os.environ:
        levels_str = os.environ["OPENEO_PROCESS_LEVELS"]

    if isinstance(levels_str, str) and len(levels_str) > 0:
        _log.info(f"Testing process levels {levels_str!r}")
        return list(map(lambda l: l.strip(), levels_str.split(",")))
    else:
        return []


@pytest.fixture(scope="session")
def processes(request) -> List[str]:
    """
    Fixture to get the desired processes to test against.
    """
    processes_str = ""
    # TODO: also support getting it from a config file?
    if request.config.getoption("--processes"):
        processes_str = request.config.getoption("--processes")
    elif "OPENEO_PROCESSES" in os.environ:
        processes_str = os.environ["OPENEO_PROCESSES"]

    if isinstance(processes_str, str) and len(processes_str) > 0:
        _log.info(f"Testing processes {processes_str!r}")
        return list(map(lambda p: p.strip(), processes_str.split(",")))
    else:
        return []


@pytest.fixture(scope="module")
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return False


@pytest.fixture(scope="module")
def connection(request, auto_authenticate: bool, pytestconfig) -> openeo.Connection:
    backend_url = get_backend_url(request.config, required=True)
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
            # Note: this is based on `capfd.disabled()`, but compatible with a wide fixture scopes (e.g. session or module)
            capmanager = pytestconfig.pluginmanager.getplugin("capturemanager")
            with capmanager.global_and_fixture_disabled():
                # Note: this generic `authenticate_oidc()` call allows both:
                # - device code/refresh token based authentication for manual test suite runs
                # - client credentials auth through env vars for automated/Jenkins CI runs
                #
                # See https://open-eo.github.io/openeo-python-client/auth.html#oidc-authentication-dynamic-method-selection
                con.authenticate_oidc()

    return con


@pytest.fixture
def skipper(connection, process_levels) -> Skipper:
    return Skipper(connection=connection, process_levels=process_levels)
