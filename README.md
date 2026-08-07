
# openEO Test Suite

Test suite for validation of openEO back-ends against the openEO API and related specifications.

Location: https://github.com/Open-EO/openeo-test-suite

## Project structure and modular design

The openEO test suite was developed in separate work packages,
which is roughly reflected in the project structure.
The separate modules allow to run the test suite in a more fine-grained way,
focussing on a specific API aspect to test or verify
(e.g. just collection metadata validation or individual process testing).


> **Note**
> In the following overview includes some invocation examples that are given as basic reference.
> Make sure to also check the more [detailed documentation of the test run options](#run-options) further in the docs.


- **WP1 General test suite framework** (lead implementation partner: VITO)
  - Main location: [`src/openeo_test_suite/lib`](./src/openeo_test_suite/lib)
  - Provides various reusable utilities and helpers to power the openEO test suite,
    and defines a pytest plugin to properly hook into the various phases of the pytest framework.
  - This module also defines some "internal" tests that are just meant to test these utilities in isolation,
    but it is not part of the openEO test suite itself:
    ```bash
    pytest src/openeo_test_suite/lib/internal-tests
    ```
- **WP2 Validation of collection metadata** (lead implementation partner: EURAC)
  - Main location: [`src/openeo_test_suite/tests/collections`](./src/openeo_test_suite/tests/collections)
  - Defines tests to validate openEO collection metadata against specs like
    the [openEO API](https://openeo.org/) and [STAC](https://stacspec.org/en).
  - Usage example of just running these tests against a desired openEO backend URL:
    ```bash
    pytest src/openeo_test_suite/tests/collections \
        -U https://openeo.example \
        --html=reports/collection-metadata.html
    ```
- **WP3 Validation of process metadata** (lead implementation partner: EODC)
  - Main location: [`src/openeo_test_suite/tests/processes/metadata`](./src/openeo_test_suite/tests/processes/metadata)
  - Defines tests to validate openEO process metadata against specs
    defined in the [openeo-processes](https://github.com/Open-EO/openeo-processes) project
    - Functional tests concern actual values and behavior of processes (like parameters and return values),
      failures in these tests should be looked into and fixed.
    - Non-functional tests concern descriptions and other metadata of processes that have no impact on the actual behavior of the process,
      failures in these tests should be taken as warnings, but don't necessarily need to be fixed. These can be skipped by adding
      `-m "not optional"` to the pytest command.
  - Usage example for running these tests against a desired openEO backend URL:
    ```bash
    pytest src/openeo_test_suite/tests/processes/metadata \
        -U https://openeo.example \
        -m "not optional" \
        --html=reports/process-metadata.html
    ```
- **WP4 General openEO API compliance validation** (lead implementation partner: EODC)
  - Main location: [`src/openeo_test_suite/tests/general`](./src/openeo_test_suite/tests/general)
  - Provides tests to validate the general openEO API compliance of a back-end.
  - The backend is checked against the openeo API specification defined in the [openeo-api](https://github.com/Open-EO/openeo-api/) project.
  - There are some tests which might run for a long time (as they execute actual process graphs on the backends)
    these can be skipped by adding `-m "not longrunning"` to the pytest command.
  - Usage example of just running these tests against a desired openEO backend URL:
    ```bash
    pytest src/openeo_test_suite/tests/general \
      -U https://openeo.example \
      --html=reports/general.html
    ```
  - Usage example of testing if the back-end satisfy the required [process profiles](https://openeo.org/documentation/1.0/developers/profiles/processes.html):
    ```bash
    pytest src/openeo_test_suite/tests/general \
      -U https://openeo.example \
      src/openeo_test_suite/tests/general/test_process_profile_validation.py \
      --process-levels=L1,L2,L2A,L2B,L3-Clim
    ```
- **WP5 Individual process testing** (lead implementation partner: M. Mohr)
  - Main location: [`src/openeo_test_suite/tests/processes/processing`](./src/openeo_test_suite/tests/processes/processing)
  - Provides tests to validate individual openEO processes,
    based on the expected input-output examples
    defined in the [openeo-processes](https://github.com/Open-EO/openeo-processes) project
    under [Open-EO/openeo-processes#468](https://github.com/Open-EO/openeo-processes/pull/468)
  - Very basic usage example of just running these tests:
    ```bash
    pytest src/openeo_test_suite/tests/processes/processing \
        --html=reports/individual-processes.html
    ```
    Note that this invocation will not actually execute anything,
    see [WP5 Specifics](#wp5-specifics) for more information and functional examples.
- **WP6 Full process graph execution and validation** (lead implementation partner: EURAC)
  - Main location: [`src/openeo_test_suite/tests/workflows`](./src/openeo_test_suite/tests/workflows)
  - Provides tests to run full processes graphs and evaluate the results.
  - Usage example of just running these tests against a desired openEO backend URL:
    ```bash
    pytest src/openeo_test_suite/tests/workflows \
        -U https://openeo.example \
        --s2-collection SENTINEL2_L2A \
        --html=reports/workflows.html
    ```
   - See [WP6 Specifics](#wp6-specifics) for some more details and examples.


## Installation and setup

Clone this repository and some git submodules with additional assets/data, e.g.:

```bash
git clone --recurse-submodules https://github.com/Open-EO/openeo-test-suite.git
```

As always in Python usage and development,
it is recommended to work in some sort of virtual environment (`venv`, `virtualenv`, `conda`, `docker`, ...)
to run and develop this project.
Depending on your use case and workflow, you can choose to reuse an existing environment or create a new one.

### Example virtual environment setup

Python's standard library includes a [`venv` module](https://docs.python.org/3/library/venv.html)
to create virtual environments.
A common practice is to create a virtual environment in a subdirectory `venv` of your project,
which can be achieved by running this from the project root:

```bash
python -m venv --prompt . venv
```

Note: the `--prompt .` option is a trick to automatically
use the project root directory name in your shell prompt
when the virtual environment is activated.
It's optional, but it generally makes your life easier
when you have multiple virtual environments on your system.

### Virtual environment activation

The following instructions will assume that the virtual environment of your choosing is activated.
For example, when using the `venv` approach from above,
activate the virtual environment in your shell with:

```bash
source venv/bin/activate
```

### Install `openeo-test-suite` package (with dependencies)

Install the project and its dependencies in your virtual environment with:

```bash
pip install -e .
```

Note: the `-e` option installs the project in "editable" mode,
which makes sure that code changes will be reflected immediately in your virtual environment
without the need of (re)installing the project.


### Additional optional dependencies related to runners for individual process testing <a name="runner-dependencies"></a>

The individual process testing module of the test suite allows to pick
a specific process "runner" (see [WP5 specifics](#wp5-specifics) for more documentation).
Some of these runners require additional optional dependencies to be installed in your virtual environment,
which can be done by providing an appropriate "extra" identifier in the `pip install` command:

- For the "dask" runner:
    ```bash
    pip install -e .[dask]
    ```
- For the "vito" runner:
    ```bash
    pip install -e .[vito]
    ```

Note that it might be not possible to install both "dask" and "vito" extras
seamlessly in the same environment because of conflicting dependency constraints.


## Test suite run options <a name="run-options"></a>

Most modules of the test suite at least require an openEO backend URL to run against.
It can be specified through a `pytest` command line option:

    pytest --openeo-backend-url=openeo.example

    # Or using the short form `-U` (at the cost of being less descriptive):
    pytest -U openeo.example

If no explicit protocol is specified, `https://` will be assumed automatically.

### Process selection

Various tests depend on the availability of certain openEO processes.
It is possible to only run tests for a subset of processes with these
process selection options:

- `--processes` to define a comma-separated list of processes to test against.
  - Example: `--processes=min,load_stac,apply,reduce_dimension`.
  - Note that processes specified with this option are always selected,
    irrespective of their "experimental" status
    and the presence of the `--experimental` option discussed below.
- `--process-levels` to select whole groups of processes based on
  predefined [process profiles](https://openeo.org/documentation/1.0/developers/profiles/processes.html),
  specified as a comma-separated list of levels.
  - Example: `--process-levels=L1,L2`.`
  - A level does not imply other levels, so each desired level must be specified explicitly.
    For example, L2 does **not** include L1 automatically.

If neither `--processes` nor `--process-levels` are specified, all processes are considered.
If both are specified, the union of both will be considered.

- `--experimental`: By default, experimental processes (or experimental process tests) are ignored.
  Enabling this option will consider experimental processes and tests.
  Note that experimental processes explicitly selected with `--processes` will be
  kept irrespective of this option.


### Recommended `pytest` options

pytest provides a [lot of command-line options](https://docs.pytest.org/en/8.0.x/reference/reference.html#command-line-flags)
to fine-tune how the test suite is executed (test selection, reporting, ...).
Some recommended options to use in practice:

- `-vv`: increase verbosity while running the test,
  e.g. to have a better idea of the progress of slow tests.
- `--tb=short`/`--tb=line`/`--tb=no`: avoid output of full stack traces,
  which give little to no added value for some test modules.


### Authentication of the basic `connection` fixture

The test suite provides a basic `connection` fixture
(an `openeo.Connection` object as defined in the `openeo` Python library package)
to interact with the backend.

There are several ways to set up authentication for this connection fixture,
building on the ["dynamic authentication method selection" feature of the `openeo` Python library package](https://open-eo.github.io/openeo-python-client/auth.html#oidc-authentication-dynamic-method-selection),
which is driven by the `OPENEO_AUTH_METHOD` environment variable:

- `OPENEO_AUTH_METHOD=none`: no authentication will be done
- `OPENEO_AUTH_METHOD=basic`: basic authentication will be triggered.
  Username and password can be specified through additional environment variables
  `OPENEO_AUTH_BASIC_USERNAME`, and `OPENEO_AUTH_BASIC_PASSWORD`.
  Alternatively, it is also possible to handle basic auth credentials through
  the [auth configuration system and `openeo-auth` tool](https://open-eo.github.io/openeo-python-client/auth.html#auth-config-files-and-openeo-auth-helper-tool)
  from the `openeo` Python library package.
- `OPENEO_AUTH_METHOD=client_credentials`: OIDC with "client credentials" grant,
  which [assumes some additional environment variables to set the client credentials](https://open-eo.github.io/openeo-python-client/auth.html#oidc-client-credentials-using-environment-variables).
- If nothing is specified (the default), the default behavior of `connection.authenticate_oidc()` is followed:
  - Valid OIDC refresh tokens will be used if available
  - Otherwise, the OIDC device code flow is initiated.
    Make sure to check the logging/output of the test suite run
    for instructions on how to complete the authentication flow.


## Test module specifics

Some test modules have specific considerations and options to be aware of.


### WP5. Individual process testing: process runners <a name="wp5-specifics"></a>

The goal of the **individual process testing** module of the test suite
is testing each openEO process individually with one or more pairs of input and expected output.
Because there are a lot of these tests (order of thousands),
it is very time-consuming to run these through the standard, HTTP based openEO REST API.
As a countermeasure, the test suite ships with several experimental **runners**
that aim to execute the tests directly against a (locally running) back-end implementation
to eliminate HTTP-related and other overhead.
Note that this typically requires additional dependencies to be installed in your test environment.

The desired runner can be specified through the `--runner` option,
with currently one of the following options:

- `skip` (**default**): Skip all individual process tests.
  - This is the default to avoid accidentally running a very heavy/costly test suite.
- `http`: Run the individual processing tests through a standard openEO REST API.
  - Requires `--openeo-backend-url` to be set as described above.
  - As noted above, this will very likely result a very heavy test suite run by default.
    It is therefore recommended to limit the test suite scope
    in some way: e.g. limited process selection through `--processes`
    or running against a dedicated/localhost deployment.
  - Another limitation of this runner is that not all process tests
    can be executed as some input-output pairs are not JSON encodable.
    These tests will be marked as skipped.
- `dask`: Executes the tests directly via the [openEO Dask implementation](https://github.com/Open-EO/openeo-processes-dask) (as used by EODC, EURAC, and others)
  - Requires [openeo_processes_dask](https://github.com/Open-EO/openeo-processes-dask) package being installed in test environment.
    See [installation instructions](#runner-dependencies) above for more practical info.
  - Covers all implemented processes.
- `vito`: Executes the tests directly via the
  [openEO Python Driver implementation](https://github.com/Open-EO/openeo-python-driver) (as used by CDSE, VITO/Terrascope, and others).
  - Requires [openeo_driver](https://github.com/Open-EO/openeo-python-driver) package being installed in test environment.
    See [installation instructions](#runner-dependencies) above for more practical info.
  - Only covers a subset of processes due to the underlying architecture of the back-end implementation.
    In particular, it only covers the pure Python code paths, but not the PySpark related aspects.

See [openeo_test_suite/lib/process_runner](./src/openeo_test_suite/lib/process_runner)
for more details about these runners and inspiration to implement your own runner.



#### Usage examples of individual process testing with runner option

The individual process tests can be run by specifying the `src/openeo_test_suite/tests/processes/processing` as test path.
Some use examples with different options discussed above:

```bash
# Basic default behavior: run all individual process tests,
# but with the default runner (skip), so no tests will actually be executed.
pytest src/openeo_test_suite/tests/processes

# Run tests for a subset of processes with the HTTP runner
# against the openEO Platform backend at openeo.cloud
pytest --runner=http --openeo-backend-url=openeo.cloud \
    --processes=min,max \
    src/openeo_test_suite/tests/processes/processing

# Run tests for a subset of processes with the VITO runner
pytest --runner=vito --process-levels=L1,L2,L2A \
    src/openeo_test_suite/tests/processes/processing

# Run all individual process tests with the Dask runner
pytest --runner=dask src/openeo_test_suite/tests/processes
```



### WP6. Full process graph execution and validation <a name="wp6-specifics"></a>

These tests are designed to run using synchronous openEO process calls
and a Sentinel-2(-like) collection.

The S2 collection to use must be specified through the `--s2-collection` option,
which supports two forms:

- a normal openEO collection name (e.g. `--s2-collection=SENTINEL2_L2A`)
  which will be loaded through the standard openEO `load_collection` process.
- a STAC URL (typically starting with `https://`),
  which will be loaded with `load_stac`.

  The following two example STAC collections are provided in the context of this test suite project.
  Each of these exists to cater to subtle differences between some back-end implementations
  regarding temporal and band dimension naming and how that is handled in `load_stac`.
   - https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE:
     defines `"t"` as temporal dimension name, and `"bands"` as bands dimension name.
     Recommended to be used with VITO/CDSE openEO backends.
   - https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE_2:
     uses `"time"` as temporal dimension name, and `"band"` as bands dimension name.
     Recommended to be used with EURAC and EODC openEO backends.

If the back-end does not support `load_stac`, a collection name must be used.

#### Usage examples:

```bash
# Compact
pytest src/openeo_test_suite/tests/workflows \
    -U openeo.dataspace.copernicus.eu \
    --s2-collection=SENTINEL2_L2A

# With full back-end URL,
# a STAC collection to use instead of a predefined openEO collection
# and a list of process levels to test against
pytest src/openeo_test_suite/tests/workflows \
    --openeo-backend-url=https://openeo.dataspace.copernicus.eu/openeo/1.2 \
    --s2-collection=https://stac.eurac.edu/collections/SENTINEL2_L2A_SAMPLE \
    --process-levels=L1,L2
```




## Reporting

Being a `pytest` based test suite, various plugins can be used to generate reports in different formats as desired.

### HTML report

Producing reports in HTML format is enabled by default (using the `pytest-html` plugin).
Basic usage example
(note that this usually has to be combined with other `pytests` options commented elsewhere in this document):

    pytest --html=reports/report.html

### JUnitXML report

JUnitXML reports are useful for integration with CI systems like Jenkins.
Support for it is built-in in `pytest` through the `--junit-xml` option:

    pytest --junit-xml=reports/report.xml


## Extending the test suite and adding new tests

How to extend the test suite depends largely on the module or aspect you want to extend.
Some general guidelines:

- General test suite framework: add new functionality or extend existing utilities
  `src/openeo_test_suite/lib`. Preferably also add "internal" tests,
  which should be able to run without the presence of a real openEO backend.
- Validation of collection metadata:
  extend existing tests or add new tests at `src/openeo_test_suite/tests/collections`.
- Validation of process metadata:
  add new tests to `src/openeo_test_suite/tests/processes/metadata`.
- General openEO API compliance validation:
  add new tests to `src/openeo_test_suite/tests/general`.
- Individual process testing:
  - new input-output pairs for existing or new processes:
    add them in the [openeo-processes](https://github.com/Open-EO/openeo-processes) project
    or under [Open-EO/openeo-processes#468](https://github.com/Open-EO/openeo-processes/pull/468)
  - extend functionality (e.g. process runners, data conversion aspects, ...):
    see [openeo_test_suite/lib/process_runner](./src/openeo_test_suite/lib/process_runner)
- Full process graph execution and validation:
  add new tests to `src/openeo_test_suite/tests/workflows`,
  use existing tests there as inspiration on how to write new tests.


## Development and contributions

The test suite builds on [`pytest`](https://pytest.org/),
a featureful testing library for Python that makes it easy to write succinct, readable tests
and can scale to support complex functional testing.
It has some particular features (fixtures, leveraging the `assert` statement, test parameterization, ...)
that are worth getting familiar with.

### Pre-commit hooks

This project provides (git) pre-commit hooks to tidy up simple code quality problems and catch syntax issues before committing.
While not enforced, it is encouraged and appreciated to enable this in your working copy before contributing code.

#### Pre-commit Setup

- Install the general [pre-commit](https://pre-commit.com/) tool.
  The simplest option is to install it directly in the virtual environment you are using for this project (e.g. `pip install pre-commit`)
  You can also install it globally
  (e.g. using a package manager like [pipx](https://pypa.github.io/pipx/), conda, homebrew, ...)
  so you can use this tool across different projects.
- Install the project specific git hook scripts and utilities
  (defined in the `.pre-commit-config.yaml` configuration file)
  by running this in the root of your working copy:

      pre-commit install

#### Pre-commit Usage

When you commit new changes, the pre-commit hook will automatically run each of the configured linters/formatters/...
Some of these just flag issues (e.g. invalid JSON files) while others even automatically fix problems (e.g. clean up excessive whitespace).
If there is some kind of violation, the commit will be blocked. Address these problems and try to commit again.

Some pre-commit tools directly edit your files (e.g. fix code style) instead of just flagging issues.
This might feel intrusive at first, but once you get the hang of it, it should allow to streamline your development workflow.
In particular, it is recommended to use git's staging feature to prepare your commit.
Pre-commit’s proposed changes are not staged automatically, so you can more easily keep them separate for review.

> **Note**
> You can temporarily disable pre-commit for these rare cases where you intentionally want to commit violating code style,
> e.g. through git commit command line option `-n/--no-verify`.
