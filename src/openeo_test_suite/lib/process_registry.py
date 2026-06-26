import itertools
import json
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional, Union

import json5

import openeo_test_suite

_log = logging.getLogger(__name__)


@dataclass(frozen=True)
class ProcessData:
    """Process data, including profile level and list of tests"""

    process_id: str
    spec: dict
    level: str
    tests: List[dict]  # TODO: also make dataclass for each test?
    experimental: bool
    path: Path


class ProcessRegistry:
    """
    Registry of processes, metadata (level, experimental flag)
    and related tests defined in openeo-processes project
    """

    def __init__(self, root: Optional[Path] = None):
        """
        :param root: Root directory of the tests folder in  openeo-processes project
        """

        self._root = Path(root or self._guess_root())
        self._root_json5 = Path(self._root.joinpath("tests"))

        # Lazy load cache
        self._processes: Union[None, List[ProcessData]] = None

    def _guess_root(self):
        # TODO: avoid need for guessing and properly include assets in (installed) package
        project_root = Path(openeo_test_suite.__file__).parents[2]
        candidates = [
            project_root / "assets/processes",
            Path("./assets/processes"),
            Path("./openeo-test-suite/assets/processes"),
        ]
        for candidate in candidates:
            if candidate.exists() and candidate.is_dir():
                return candidate
        raise ValueError(
            f"Could not find valid processes test root directory (tried {candidates})"
        )

    def _load(self) -> Iterator[ProcessData]:
        """Collect all processes"""
        # TODO: cache or preload this in __init__? Or even reuse across instances?
        if not self._root.is_dir():
            raise ValueError(f"Invalid process test root directory: {self._root}")
        _log.info(f"Loading process definitions from {self._root}")

        process_paths = itertools.chain(
            self._root.glob("*.json"), self._root.glob("proposals/*.json")
        )
        for path in process_paths:
            test_metadata_path = self._root_json5 / f"{path.stem}.json5"
            try:
                with path.open() as f:
                    data = json.load(f)
                if data["id"] != path.stem:
                    raise ValueError(
                        f"Process id mismatch between id {data['id']!r} and filename {path.name!r}"
                    )
                # Metadata is stored in sibling json file
                if test_metadata_path.exists():
                    with test_metadata_path.open() as f:
                        metadata = json5.load(f)
                else:
                    metadata = {}

                yield ProcessData(
                    process_id=data["id"],
                    spec=data,
                    level=metadata.get(
                        "level", "L4"
                    ),  # default to L4 is intended for processes without a specific level
                    tests=metadata.get("tests", []),
                    experimental=data.get("experimental", False),
                    path=path,
                )
            except Exception as e:
                # TODO: good idea to skip broken definitions? Why not just fail hard?
                _log.error(f"Failed to load process data from {path}: {e!r}")

    def get_all_processes(self) -> Iterable[ProcessData]:
        if self._processes is None:
            self._processes = list(self._load())
        return iter(self._processes)

    def get_processes_filtered(
        self,
        process_ids: Optional[List[str]] = None,
        process_levels: Optional[List[str]] = None,
        experimental: bool = False,
    ) -> Iterator[ProcessData]:
        """
        Collect processes matching with additional filtering:

        :param process_ids: allow list of process ids (empty/None means allow all)
        :param process_levels: allow list of process levels (empty/None means allow all)
        :param experimental: allow experimental processes or not?
        """
        for process_data in self.get_all_processes():
            pid = process_data.process_id
            level = process_data.level

            if process_ids and pid in process_ids:
                yield process_data
            elif process_levels and level in process_levels:
                if process_data.experimental and not experimental:
                    _log.debug(f"Skipping process {pid!r}: experimental")
                    continue
                yield process_data
            elif not process_ids and not process_levels:
                # No id or level allow lists: no filtering (except experimental flag)
                if process_data.experimental and not experimental:
                    _log.debug(f"Skipping process {pid!r}: experimental")
                    continue

                yield process_data
            else:
                _log.debug(
                    f"Skipping process {pid!r}: not in allow lists {process_levels=} or {process_ids=}"
                )

    def get_process(self, process_id: str) -> ProcessData:
        for process_data in self.get_all_processes():
            if process_data.process_id == process_id:
                return process_data
        raise LookupError(f"Process not found: {process_id!r}")
