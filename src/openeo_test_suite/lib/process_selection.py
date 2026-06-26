import functools
import logging
from dataclasses import dataclass
from typing import List, Optional, Union

import pytest

from openeo_test_suite.lib.process_registry import ProcessData, ProcessRegistry

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProcessFilters:
    """
    Container for process filters as specified through command line options
    `--processes`,`--process-level`, `--experimental`
    """

    process_ids: Optional[List[str]] = None
    process_levels: Optional[List[str]] = None
    experimental: bool = False


# Internal singleton pointing to active set of process filters
# setup happens in `pytest_configure` hook
_process_filters: Union[ProcessFilters, None] = None


def set_process_selection_from_config(config: pytest.Config):
    """Set up process selection from pytest config (CLI options)."""
    global _process_filters
    assert _process_filters is None
    _process_filters = ProcessFilters(
        process_ids=csv_to_list(config.getoption("--processes"), none_on_empty=True),
        process_levels=csv_to_list(
            config.getoption("--process-levels"), none_on_empty=True
        ),
        experimental=config.getoption("--experimental"),
    )


# TODO: more structural/testable solution for get_selected_processes related caching?
@functools.lru_cache()
def get_selected_processes() -> List[ProcessData]:
    """
    Get effective list of processes extracted from the process registry
    with filtering based on command line options
    `--processes`,`--process-level`, `--experimental`
    """
    global _process_filters
    assert isinstance(_process_filters, ProcessFilters)

    return list(
        ProcessRegistry().get_processes_filtered(
            process_ids=_process_filters.process_ids,
            process_levels=_process_filters.process_levels,
            experimental=_process_filters.experimental,
        )
    )


def csv_to_list(
    csv: Union[str, None] = None, *, separator: str = ",", none_on_empty: bool = False
) -> Union[List[str], None]:
    """
    Convert comma-separated string to list of strings,
    properly taking care of trailing whitespace, empty items, ...
    """
    # TODO: options to disable stripping, or to allow empty items?
    items = [item.strip() for item in (csv or "").split(separator) if item.strip()]
    if not items and none_on_empty:
        return None
    return items
