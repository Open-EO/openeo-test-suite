import logging
import os

import openeo
import pytest

from openeo_test_suite.lib.process_runner.base import ProcessTestRunner

_log = logging.getLogger(__name__)


@pytest.fixture(scope="session")
def runner(request) -> str:
    """
    Fixture to get the desired runner to test with.
    """
    # TODO: also support getting it from a config file?
    if request.config.getoption("--runner"):
        runner = request.config.getoption("--runner")
    elif "OPENEO_RUNNER" in os.environ:
        runner = os.environ["OPENEO_RUNNER"]
    else:
        runner = "http"

    _log.info(f"Using runner {runner!r}")

    return runner


@pytest.fixture(scope="module")
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return True


@pytest.fixture(scope="module")
def connection(
    backend_url: str, runner: str, auto_authenticate: bool, pytestconfig
) -> ProcessTestRunner:
    # TODO: avoid overriding existing "connection" fixture with a different kind of object (ProcessTestRunner)
    if runner == "dask":
        from openeo_test_suite.lib.process_runner.dask import Dask

        return Dask()
    elif runner == "vito":
        from openeo_test_suite.lib.process_runner.vito import Vito

        return Vito()
    else:
        from openeo_test_suite.lib.process_runner.http import Http

        con = openeo.connect(backend_url)
        if auto_authenticate:
            # Temporarily disable output capturing, to make sure that OIDC device code instructions (if any) are visible to the user.
            # Note: this is based on `capfd.disabled()`, but compatible with a wide fixture scopes (e.g. session or module)
            capmanager = pytestconfig.pluginmanager.getplugin("capturemanager")
            with capmanager.global_and_fixture_disabled():
                con.authenticate_oidc()

        return Http(con)
