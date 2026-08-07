# """
# Tests to validate that the processes exposed at the backend's /processes endpoint
# satisfy the profiles requirements as defined in the openEO specification.

# Reference: https://openeo.org/documentation/1.0/developers/profiles/processes.html#requirements-per-profile
# """

import pytest
import logging
from openeo_test_suite.lib.process_registry import ProcessRegistry
from openeo_test_suite.lib.process_selection import get_selected_processes

_log = logging.getLogger(__name__)


@pytest.fixture
def selected_process_levels(request) -> set:
    """
    Extract process levels from the command-line option --process-levels.
    
    Returns:
        Set of process level strings (e.g., {'L1', 'L2'})
    """
    process_levels_str = request.config.getoption("--process-levels")
    if not process_levels_str:
        # If no levels specified, return empty set (all processes)
        return set()
    
    levels = {level.strip() for level in process_levels_str.split(",") if level.strip()}
    return levels


def test_profile_processes_available(backend_processes_names, selected_process_levels):
    """
    Test that all required processes for selected profile levels are available at the backend.
    
    Uses the --process-levels command-line parameter to determine which profiles to validate.
    If --process-levels is not specified, this test is skipped.
    
    Example usage:
        pytest test_file.py --process-levels=L1,L2 -U https://backend.example
    """
    
    if not selected_process_levels:
        pytest.skip("No process levels specified via --process-levels parameter")
    
    # Get all selected processes from the registry based on command-line filters
    selected_processes = get_selected_processes()
    
    # Filter to only processes in the specified levels
    level_processes = [
        p for p in selected_processes 
        if any(level in p.level for level in selected_process_levels)
    ]
    
    required_processes = {p.process_id for p in level_processes}
    
    if len(required_processes)==0:
        pytest.skip(f"No processes found for selected level {selected_process_levels}")

    missing_processes = required_processes - backend_processes_names
    
    # Report which levels are being tested
    tested_levels = ", ".join(sorted(selected_process_levels))
    
    assert len(missing_processes) == 0, (
        f"Backend is missing the following processes from profile(s) {tested_levels}: {sorted(missing_processes)}\n"
        f"Available processes: {sorted(backend_processes_names)}"
    )
    
    _log.info(
        f"✓ All {len(required_processes)} processes from profile(s) {tested_levels} are available"
    )