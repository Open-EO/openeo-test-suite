from typing import Dict, List

import pytest

from openeo_test_suite.lib.process_runner.base import ProcessTestRunner


class SkippingRunner(ProcessTestRunner):
    def list_processes(self) -> List[Dict]:
        pytest.skip(f"SkippingRunner: No processes")

    def execute(self, id, arguments):
        pytest.skip(f"SkippingRunner: skip executing process {id}")
