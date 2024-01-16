from typing import Any, Dict, List


class ProcessTestRunner:
    def list_processes(self) -> List[Dict]:
        """
        Returns a list of all processes supported by the backend
        Follows definition of the same function in the openEO Python client
        """
        pass

    def describe_process(self, process_id: str) -> Dict:
        """
        Returns single process description
        Follows definition of the same function in the openEO Python client
        """
        pass

    def execute(self, id: str, arguments: Dict) -> Any:
        """
        Executes a process with the given id and arguments.
        """
        pass

    def encode_process_graph(
        self, process: Dict, parent_process_id=None, parent_parameter=None
    ) -> Any:
        """
        Converts a process graph from the JSON object representation to the internal
        backend representation.
        specification -> backend
        """
        pass

    def encode_labeled_array(self, data: Dict) -> Any:
        """
        Converts a labeled array from the JSON object representation (type: labeled-array)
        to the internal backend representation openEO process tests.
        specification -> backend
        """
        raise NotImplementedError("labeled arrays not implemented yet")

    def encode_datacube(self, data: Dict) -> Any:
        """
        Converts a datacube from the JSON object representation (type: datacube) to the
        internal backend representation openEO process tests.
        specification -> backend
        """
        raise NotImplementedError("datacubes not implemented yet")

    def encode_data(self, data: Any) -> Any:
        """
        Converts data from the process test/JSON5 representation to the internal backend representation,
        excluding datacubes and labeled arrays.
        For example: JSON data types to numpy arrays.
        openEO process tests specification -> backend
        """
        return data

    def decode_data(self, data: Any, expected: Any) -> Any:
        """
        Converts data from the internal backend representation to the process test/JSON5 representation.
        For example: numpy values to JSON data types, labeled-array or datacube to
        JSON object representation.
        backend -> openEO process tests specification
        """
        return data

    def is_json_only(self) -> bool:
        """
        Defines whether the backend only supports JSON input or not.
        If True, the runner will skip all tests that contain non JSON values such as infinity and NaN.
        """
        return False

    def get_nodata_value(self) -> Any:
        """
        Returns the nodata value of the backend.
        """
        return None
