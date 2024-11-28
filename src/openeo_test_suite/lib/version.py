import json
import logging
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Union

import openeo_test_suite

_log = logging.getLogger(__name__)


_ON_ERROR_IGNORE = "ignore"
_ON_ERROR_WARN = "warn"
_ON_ERROR_FAIL = "fail"


# TODO: make this compatible with packaging?
PROJECT_ROOT = Path(openeo_test_suite.__file__).parents[2]


def get_openeo_versions() -> Dict[str, str]:
    return {
        "openeo-test-suite": get_openeo_test_suite_version(name_prefix=None),
        "openeo-api": get_openeo_api_spec_version(name_prefix=None),
        "openeo-processes": get_openeo_processes_spec_version(name_prefix=None),
    }


def _join_non_empties(*parts: str, glue: str = " ") -> str:
    """Join non-empty parts"""
    return glue.join(p for p in parts if p)


def get_openeo_test_suite_version(
    *,
    name_prefix: Optional[str] = "openeo-test-suite",
    on_error: str = _ON_ERROR_WARN,
    git_describe: bool = True,
) -> str:
    """Build openeo-test-suite version, optionally with name prefix and git rev suffix (if possible)"""
    return _join_non_empties(
        name_prefix,
        openeo_test_suite.__version__,
        _git_describe(PROJECT_ROOT, on_error=on_error) if git_describe else None,
    )


def get_openeo_api_spec_version(
    *,
    name_prefix: Optional[str] = "openeo-api",
    on_error: str = _ON_ERROR_WARN,
    git_describe: bool = True,
) -> str:
    """Build version of current openeo-api submodule, optionally with name prefix and git rev suffix (if possible)"""
    package_path = PROJECT_ROOT / "assets" / "openeo-api" / "package.json"
    return _join_non_empties(
        name_prefix,
        _get_js_package_version(package_path, on_error=on_error),
        _git_describe(package_path, on_error=on_error) if git_describe else None,
    )


def get_openeo_processes_spec_version(
    *,
    name_prefix: Optional[str] = "openeo-processes",
    on_error: str = _ON_ERROR_WARN,
    git_describe: bool = True,
) -> str:
    """Build version of current openeo-processes submodule, optionally with name prefix and git rev suffix (if possible)"""
    package_path = PROJECT_ROOT / "assets" / "processes" / "dev" / "package.json"
    return _join_non_empties(
        name_prefix,
        _get_js_package_version(package_path, on_error=on_error),
        _git_describe(package_path, on_error=on_error) if git_describe else None,
    )


def _get_js_package_version(
    package_path: Path, on_error: str = _ON_ERROR_WARN, default: str = "unknown"
) -> str:
    """
    Get version of a "package.json" JS project

    :param package_path: path to package.json file
    """
    try:
        package_metadata = json.loads(package_path.read_text())
        version = package_metadata["version"]
    except Exception as e:
        if on_error == _ON_ERROR_WARN:
            _log.warning(f"Failed to parse package version from {package_path}: {e}")
        elif on_error == _ON_ERROR_IGNORE:
            pass
        else:
            raise
        version = default
    return version


def _git_describe(
    path: Path, *, wrap: str = "()", on_error: str = _ON_ERROR_WARN
) -> Union[str, None]:
    """
    Get short git rev description (possibly with "dirty" indicator), e.g. 'abc123' or 'abc123-dirty'
    """
    try:
        if not path.is_dir():
            path = path.parent
        assert path.is_dir()
        command = ["git", "describe", "--always", "--dirty"]
        description = subprocess.check_output(command, cwd=path).strip().decode("utf-8")
        if wrap:
            description = f"{wrap[0]}{description}{wrap[-1]}"
    except Exception:
        if on_error == _ON_ERROR_WARN:
            _log.warning(f"Failed to git-describe {path}")
        elif on_error == _ON_ERROR_IGNORE:
            pass
        else:
            raise
        description = None
    return description
