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


@pytest.fixture(scope="session")
def process_levels(request):
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
def processes(request):
    """
    Fixture to get the desired profiles to test against.
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


@pytest.fixture
def connection(
    backend_url: str, runner: str, auto_authenticate: bool, capfd
) -> ProcessTestRunner:
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
            with capfd.disabled():
                con.authenticate_oidc()

        return Http(con)
