# Tests for (individual) processes

- tests for validation of process metadata against the [openEO API](https://openeo.org/).
- individual process testing, e.g. based on input-output examples.

## Process Metadata tests

...

## Individual Process Testing

Examples:

- `pytest --openeo-backend-url=https://openeo.cloud --processes=min,max`
- `pytest --runner=vito --process-levels=L1,L2,L2A`
- `pytest --runner=dask`

Parameters:

- `--runner`: The execution engine. One of:
  - `vito` (needs <https://github.com/Open-EO/openeo-python-driver> being installed)
  - `dask` (needs optional Dask dependencies)
  - `http` (**default**, requires `--openeo-backend-url` to be set)
- `--process-levels`: All [process profiles](https://openeo.org/documentation/1.0/developers/profiles/processes.html) to test against, separated by comma. You need to list all levels explicitly, e.g., L2 does **not** include L1 automatically. Example: `L1,L2,L2A`. By default tests against all processes.
- `--processes`: A list of processes to test against, separated by comma. Example: `apply,reduce_dimension`. By default tests against all processes.
