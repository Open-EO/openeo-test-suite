import re
import subprocess

import pytest

from openeo_test_suite.lib.version import (
    _ON_ERROR_FAIL,
    _ON_ERROR_IGNORE,
    _ON_ERROR_WARN,
    PROJECT_ROOT,
    _get_js_package_version,
    _git_describe,
    get_openeo_api_spec_version,
    get_openeo_processes_spec_version,
    get_openeo_test_suite_version,
)


def test_get_openeo_test_suite_version():
    assert re.fullmatch(
        r"openeo-test-suite [0-9.]+ \([0-9a-f]+(-dirty)?\)",
        get_openeo_test_suite_version(),
    )
    assert re.fullmatch(
        r"[0-9.]+ \([0-9a-f]+(-dirty)?\)",
        get_openeo_test_suite_version(name_prefix=None),
    )
    assert re.fullmatch(
        r"[0-9.]+", get_openeo_test_suite_version(name_prefix=None, git_describe=False)
    )


def test_get_openeo_api_spec_version():
    assert re.fullmatch(
        r"openeo-api [0-9.a-z-]+ \([0-9a-f]+\)", get_openeo_api_spec_version()
    )
    assert re.fullmatch(
        r"[0-9.a-z-]+",
        get_openeo_api_spec_version(name_prefix=None, git_describe=False),
    )


def test_get_openeo_processes_spec_version():
    assert re.fullmatch(
        r"openeo-processes [0-9.a-z-]+ \([0-9a-f]+\)",
        get_openeo_processes_spec_version(),
    )
    assert re.fullmatch(
        r"[0-9.a-z-]+",
        get_openeo_processes_spec_version(name_prefix=None, git_describe=False),
    )


def test_get_js_package_version(tmp_path):
    path = tmp_path / "package.json"
    path.write_text('{"version":"1.2.3"}')
    assert _get_js_package_version(path) == "1.2.3"


def test_get_js_package_version_on_error_default(tmp_path, caplog):
    path = tmp_path / "package.json"
    assert _get_js_package_version(path) == "unknown"
    assert "Failed to parse package version from" in caplog.text


def test_get_js_package_version_on_error_ignore(tmp_path, caplog):
    path = tmp_path / "package.json"
    assert _get_js_package_version(path, on_error=_ON_ERROR_IGNORE) == "unknown"
    assert caplog.text == ""


def test_get_js_package_version_on_error_warn(tmp_path, caplog):
    path = tmp_path / "package.json"
    assert _get_js_package_version(path, on_error=_ON_ERROR_WARN) == "unknown"
    assert "Failed to parse package version from" in caplog.text


def test_get_js_package_version_on_error_fail(tmp_path, caplog):
    path = tmp_path / "package.json"
    with pytest.raises(FileNotFoundError):
        _ = _get_js_package_version(path, on_error=_ON_ERROR_FAIL)


def test_git_describe():
    assert re.fullmatch(r"\([0-9a-f]+(-dirty)?\)", _git_describe(PROJECT_ROOT))


def test_git_describe_wrap():
    assert re.fullmatch(r"<[0-9a-f]+(-dirty)?>", _git_describe(PROJECT_ROOT, wrap="<>"))


def test_git_describe_on_error_default(tmp_path, caplog):
    assert _git_describe(tmp_path) is None
    assert "Failed to git-describe" in caplog.text


def test_git_describe_on_error_ignore(tmp_path, caplog):
    assert _git_describe(tmp_path, on_error=_ON_ERROR_IGNORE) is None
    assert caplog.text == ""


def test_git_describe_on_error_warn(tmp_path, caplog):
    assert _git_describe(tmp_path, on_error=_ON_ERROR_WARN) is None
    assert "Failed to git-describe" in caplog.text


def test_git_describe_on_error_fail(tmp_path, caplog):
    with pytest.raises(subprocess.CalledProcessError):
        _ = _git_describe(tmp_path, on_error=_ON_ERROR_FAIL)
