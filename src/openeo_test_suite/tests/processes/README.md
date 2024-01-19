# Tests for (individual) processes

- tests for validation of process metadata against the [openEO API](https://openeo.org/).
- individual process testing, e.g. based on input-output examples.

## Process Metadata tests

...

## Individual Process Testing

### Usage examples

Specify test path `src/openeo_test_suite/tests/processes/processing` to only run individual process tests.


```bash
# Basic default behavior: run all individual process tests,
# but with the default runner (skip), so no tests will actually be executed.
pytest src/openeo_test_suite/tests/processes

# Run tests for a subset of processes with the HTTP runner
# against the openEO Platform backend at openeo.cloud
pytest --runner=http --openeo-backend-url=openeo.cloud --processes=min,max src/openeo_test_suite/tests/processes/processing

# Run tests for a subset of processes with the VITO runner
pytest --runner=vito --process-levels=L1,L2,L2A src/openeo_test_suite/tests/processes/processing

# Run all individual process tests with the Dask runner
pytest --runner=dask src/openeo_test_suite/tests/processes
```

### Parameters

- `--runner`: The execution engine. One of:
  - `skip` (**default**) skip all individual process tests
  - `vito` (requires [openeo_driver](https://github.com/Open-EO/openeo-python-driver) package being installed in test environment)
  - `dask` (requires [openeo_processes_dask](https://github.com/Open-EO/openeo-processes-dask) package being installed in test environment)
  - `http` (requires `--openeo-backend-url` to be set)
- `--process-levels`: All [process profiles](https://openeo.org/documentation/1.0/developers/profiles/processes.html) to test against, separated by comma. You need to list all levels explicitly, e.g., L2 does **not** include L1 automatically. Example: `L1,L2,L2A`. By default tests against all processes.
- `--processes`: A list of processes to test against, separated by comma. Example: `apply,reduce_dimension`. By default tests against all processes.
- `--experimental`: Enables tests for experimental processes. By default experimental processes will be skipped.

### Runners

The individual process testing ships 3 experimental runners:

- [HTTP](../../lib/process_runner/http.py) (subset of processes due to JSON limitations)
  Executes all 1000 tests via the openEO API synchronously, expect 1000+ requests to hit your back-end in a short amount of time.
- [Dask](../../lib/process_runner/dask.py) (all implemented processes)
  Executes the tests directly via the [openEO Dask implementation](https://github.com/Open-EO/openeo-processes-dask) (used by EODC, EURAC, and others)
- [VITO](../../lib/process_runner/vito.py) (subset of processes due to the underlying architecture of the back-end implementation)
  Executes the tests directly via the [openEO Python Driver implementation](https://github.com/Open-EO/openeo-python-driver) (used by CDSE, VITO, and others)

You can implement your own runner by implementing the process runner base class:
<https://github.com/Open-EO/openeo-test-suite/blob/main/src/openeo_test_suite/lib/process_runner/base.py>

See the runners above for examples.
