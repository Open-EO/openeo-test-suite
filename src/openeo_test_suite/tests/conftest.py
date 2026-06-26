import argparse
import logging
import os
from typing import List

import openeo
import pytest

from openeo_test_suite.lib.backend_under_test import get_backend_url
from openeo_test_suite.lib.process_selection import get_selected_processes
from openeo_test_suite.lib.skipping import Skipper

_log = logging.getLogger(__name__)


@pytest.fixture(scope="module")
def auto_authenticate() -> bool:
    """
    Fixture to act as parameterizable toggle for authenticating the connection fixture.
    Allows per-test/folder configuration of auto-authentication.
    """
    return False


@pytest.fixture(scope="module")
def connection(
    request, auto_authenticate: bool, pytestconfig: pytest.Config
) -> openeo.Connection:
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
def skipper(connection) -> Skipper:
    return Skipper(
        connection=connection,
        selected_processes=[p.process_id for p in get_selected_processes()],
    )
