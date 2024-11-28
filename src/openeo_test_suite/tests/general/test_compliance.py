import uuid

import pytest
import requests
from openapi_core import Spec

import openeo_test_suite.lib.compliance_util as conformance_util


@pytest.fixture(scope="session")
def base_url(request):
    return conformance_util.get_base_url(request=request)


@pytest.fixture(scope="session")
def domain(request):
    return conformance_util.get_domain(request=request)


@pytest.fixture(scope="session")
def spec(request):
    return conformance_util.adjust_spec(
        conformance_util.get_spec_path(),
        conformance_util.get_base_url(request),
        conformance_util.get_domain(request),
    )


@pytest.fixture(scope="session")
def bearer_token(pytestconfig):
    bearer_token = conformance_util.get_access_token(pytestconfig)
    return f"Bearer {bearer_token}"


def test_GET_backend_info(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = ""
    test_name = "Backend Info"

    # Run through all the generic GET endpoints and test their response to a proper request.

    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_well_known(domain: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: Change server in spec
    testing: test response by API for GET requests
    cleanup: Change server back potentially
    """

    endpoint_path = "/.well-known/openeo"
    test_name = "Well known"

    # Run through all the generic GET endpoints and test their response to a proper request.

    fail_log = conformance_util.test_endpoint(
        base_url=domain, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_file_formats(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "file_formats"
    test_name = "File formats"

    # Run through all the generic GET endpoints and test their response to a proper request.
    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_conformance(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "conformance"
    test_name = "Conformance"

    # Run through all the generic GET endpoints and test their response to a proper request.
    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_udf_runtimes(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "udf_runtimes"
    test_name = "UDF runtimes"

    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_service_types(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "service_types"
    test_name = "Service Types"

    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_credentials_oidc(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "credentials/oidc"
    test_name = "OpenID Connect authentication"

    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_collections(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "collections"
    test_name = "Basic metadata for all collections"

    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_processes(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "processes"
    test_name = "List of Predefined Processes"

    fail_log = conformance_util.test_endpoint(
        base_url=base_url, endpoint_path=endpoint_path, test_name=test_name, spec=spec
    )

    assert fail_log == ""


def test_GET_me(base_url: str, spec: Spec, bearer_token: str):
    """
    tests all the generic GET endpoints that require neither setup nor cleanup

    setup: None
    testing: test response by API for GET requests
    cleanup: None

    """
    endpoint_path = "me"
    test_name = "Information about logged in user"

    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=endpoint_path,
        test_name=test_name,
        spec=spec,
        bearer_token=bearer_token,
    )

    assert fail_log == ""

    """
    setup: collect list of collection ids
    testing: test response by API for GET requests of all the collection ids
    cleanup: None

    """
    fail_log = ""

    collection_ids = [
        collection["id"]
        for collection in requests.get((f"{base_url}collections")).json()["collections"]
    ]

    # prepare list of endpoints
    special_GET_endpoints_no_auth = [
        (f"collections/{collection_id}", f"Test for collection/{collection_id}")
        for collection_id in collection_ids
    ]

    # Run through all the special GET endpoints and test their response to a proper request.
    for path, test_name in special_GET_endpoints_no_auth:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url, endpoint_path=path, test_name=test_name, spec=spec
        )

    assert fail_log == ""


def test_GET_process_graphs(base_url: str, spec: Spec, bearer_token: str):
    """
    setup: submit valid user defined processes
    testing: test response format of submitted user defined processes
    cleanup: delete submitted user defined processes
    """
    fail_log = ""
    # SETUP

    endpoint_path = "process_graphs"
    test_name = "List all user-defined processes"

    created_udp_ids = conformance_util.put_process_graphs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING
    fail_log += conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=endpoint_path,
        test_name=test_name,
        spec=spec,
        bearer_token=bearer_token,
    )

    # CLEANUP

    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_udp_ids,
    )

    assert fail_log == ""


def test_GET_process_graphs_process_id(base_url: str, spec: Spec, bearer_token: str):
    """
    setup: submit user defined processes, gather list of user defined processes
    testing: test each individual metadata response for submitted user-defined processes
    cleanup: delete user defined processes
    """
    # SETUP
    fail_log = ""

    endpoint_path = "process_graphs"

    created_udp_ids = conformance_util.put_process_graphs(
        base_url=base_url, bearer_token=bearer_token
    )

    # prepare list of endpoints
    process_GET_endpoints_auth = [
        (f"{endpoint_path}/{process_id}", f"Test for {endpoint_path}/{process_id}")
        for process_id in created_udp_ids
    ]

    # TESTING
    for prepared_endpoint_path, test_name in process_GET_endpoints_auth:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
        )

    # CLEANUP
    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_udp_ids,
    )

    assert fail_log == ""


def test_PUT_process_graphs_process_id(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: load payloads
    TESTING: PUT UDPs
    CLEANUP: DELETE UDPs
    """

    fail_log = ""

    # SETUP
    endpoint_path = "process_graphs"
    directory_path = conformance_util.get_examples_path()
    examples_directory = "put_process_graphs"

    test_name = "Store a user-defined process"

    created_udp_ids = []
    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING
    for payload in payloads:
        id = str(uuid.uuid4())
        created_udp_ids.append(id)
        prepared_endpoint_path = f"{endpoint_path}/{id}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {id}",
            spec=spec,
            payload=payload,
            bearer_token=bearer_token,
            method="PUT",
        )

    # CLEANUP

    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_udp_ids,
    )

    assert fail_log == ""


def test_DELETE_process_graphs_process_id(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: PUT UDPs
    TESTING: DELETE UDPs
    CLEANUP: None
    """
    fail_log = ""

    # SETUP
    endpoint_path = "process_graphs"

    created_udp_ids = conformance_util.put_process_graphs(
        base_url=base_url, bearer_token=bearer_token
    )

    process_graphs_DELETE_endpoints = [
        (f"{endpoint_path}/{process_id}", f"Test for {endpoint_path}/{process_id}")
        for process_id in created_udp_ids
    ]

    # TESTING
    for prepared_endpoint_path, test_name in process_graphs_DELETE_endpoints:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
            method="DELETE",
            expected_status_codes=204,
        )

    # CLEANUP

    assert fail_log == ""


def test_GET_jobs(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: post jobs
    TESTING: GET JOBS
    CLEANUP: DELETE JOBS
    """
    fail_log = ""

    # SETUP
    endpoint_path = "jobs"
    test_name = "List all batchjobs"

    created_batch_job_ids = conformance_util.post_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING

    fail_log += conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=endpoint_path,
        test_name=f"{test_name}",
        spec=spec,
        bearer_token=bearer_token,
        method="GET",
    )

    # CLEANUP

    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


def test_POST_jobs(base_url: str, spec: Spec, bearer_token: str):
    """
    setup: prepare batch jobs payloads
    testing: test posting prepared batch jobs to endpoint
    cleanup: delete posted batch jobs
    """
    fail_log = ""
    # SETUP
    endpoint_path = "jobs"
    test_name = "Creates a new batch processing task"
    directory_path = conformance_util.get_examples_path()
    examples_directory = "post_jobs"

    created_batch_job_ids = []

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING
    for payload in payloads:
        _, payload = conformance_util.set_uuid_in_job(payload)

        fail_log_entry, response = conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
            payload=payload,
            method="POST",
            expected_status_codes=201,
            return_response=True,
        )

        fail_log += fail_log_entry
        created_batch_job_ids.append(response.headers["OpenEO-Identifier"])

    # CLEANUP
    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


def test_GET_jobs_job_id(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: post jobs
    TESTING: GET job metadata of posted jobs
    CLEANUP: Delete jobs
    """
    fail_log = ""
    # SETUP

    endpoint_path = "jobs"
    test_name = "Full metadata for a batch job"

    created_batch_job_ids = conformance_util.post_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING

    for job_id in created_batch_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            method="GET",
        )

    # CLEANUP

    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


def test_PATCH_jobs_job_id(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, prepare payloads
    TESTING: PATCH jobs
    CLEANUP: DELETE jobs
    """
    fail_log = ""
    # SETUP

    endpoint_path = "jobs"
    test_name = "Modify a batch job"

    created_batch_job_ids = conformance_util.post_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    directory_path = conformance_util.get_examples_path()
    examples_directory = "patch_jobs"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING

    for job_id, payload in zip(created_batch_job_ids, payloads):
        prepared_endpoint_path = f"{endpoint_path}/{job_id}"
        _, payload = conformance_util.set_uuid_in_job(payload)
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            payload=payload,
            method="PATCH",
            expected_status_codes=204,
        )

    # CLEANUP

    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


def test_DELETE_jobs_job_id(base_url: str, spec: Spec, bearer_token: str):
    """
    setup: Post jobs
    testing: Delete posted jobs
    cleanup: None
    """
    fail_log = ""
    # SETUP
    endpoint_path = "jobs"
    test_name = "Delete specific batch job"

    created_job_ids = conformance_util.post_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING

    for job_id in created_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            method="DELETE",
            expected_status_codes=204,
        )

    # CLEANUP

    assert fail_log == ""


def test_POST_jobs_job_id_results(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: post jobs
    TESTING: start batch jobs
    CLEANUP: ??
    """
    # SETUP
    fail_log = ""

    endpoint_path = "jobs"
    endpoint_path_extra = "results"
    test_name = "Start processing a batch job"

    created_batch_job_ids = conformance_util.post_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING

    for job_id in created_batch_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}/{endpoint_path_extra}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            method="POST",
            expected_status_codes=202,
        )

    # CLEANUP

    try:
        conformance_util.delete_id_resource(
            base_url=base_url,
            endpoint_path=endpoint_path,
            bearer_token=bearer_token,
            ids=created_batch_job_ids,
        )
    except Exception as e:
        print(e)

    assert fail_log == ""


@pytest.mark.vv
@pytest.mark.longrunning
def test_GET_jobs_job_id_results(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, START jobs (POST jobs/job_id/results), Wait for jobs to be finished
    TESTING: GET job results
    CLEANUP: DELETE Jobs
    """
    fail_log = ""
    # SETUP
    endpoint_path = "jobs"
    endpoint_path_extra = "results"
    test_name = "Download results for a completed batch job"

    created_batch_job_ids = conformance_util.post_start_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING

    conformance_util.wait_job_statuses(
        base_url=base_url,
        bearer_token=bearer_token,
        job_ids=created_batch_job_ids,
        job_statuses=["finished"],
        timeout=160,
    )

    for job_id in created_batch_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}/{endpoint_path_extra}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            method="GET",
        )

    # CLEANUP

    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


def test_DELETE_jobs_job_id_results(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, Start processing jobs
    TESTING: DELETE job id results: Cancel processing jobs
    CLEANUP: Delete jobs
    """
    fail_log = ""
    # SETUP
    endpoint_path = "jobs"
    endpoint_path_extra = "results"
    test_name = "Cancel processing a batch job"

    created_batch_job_ids = conformance_util.post_start_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    conformance_util.wait_job_statuses(
        base_url=base_url,
        bearer_token=bearer_token,
        job_ids=created_batch_job_ids,
        job_statuses=["running"],
        timeout=120,
    )

    # TESTING

    for job_id in created_batch_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}/{endpoint_path_extra}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            method="DELETE",
            expected_status_codes=204,
        )

    # CLEANUP

    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


def test_GET_jobs_job_id_estimate(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, start jobs
    TESTING: GET estimates for jobs
    CLEANUP: Cancel and delete jobs
    """

    fail_log = ""

    # SETUP
    endpoint_path = "jobs"
    endpoint_path_extra = "estimate"
    test_name = "Get an estimate for a running job"

    created_batch_job_ids = conformance_util.post_start_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING

    for job_id in created_batch_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}/{endpoint_path_extra}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            method="GET",
        )

    # CLEANUP

    conformance_util.cancel_delete_jobs(
        base_url=base_url, bearer_token=bearer_token, job_ids=created_batch_job_ids
    )

    assert fail_log == ""


def test_GET_jobs_job_id_logs(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, (start? jobs)
    TESTING: GET logs for batch jobs, GET logs for batch jobs using offset
    CLEANUP: (cancel? jobs), DELETE jobs
    """
    fail_log = ""
    # SETUP

    endpoint_path = "jobs"
    endpoint_path_extra = "logs"
    test_name = "Logs for a batch job"

    created_batch_job_ids = conformance_util.post_start_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    conformance_util.wait_job_statuses(
        base_url=base_url,
        bearer_token=bearer_token,
        job_ids=created_batch_job_ids,
        job_statuses=["running"],
    )
    # TESTING

    for job_id in created_batch_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}/{endpoint_path_extra}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            method="GET",
        )
    # CLEANUP

    conformance_util.cancel_delete_jobs(
        base_url=base_url, bearer_token=bearer_token, job_ids=created_batch_job_ids
    )

    assert fail_log == ""


@pytest.mark.longrunning
def test_POST_result(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: gather payloads
    TESTING: POST payloads to result
    CLEANUP: None
    """
    fail_log = ""

    # SETUP

    endpoint_path = "result"
    test_name = "Process and download data synchronously"

    directory_path = conformance_util.get_examples_path()
    examples_directory = "post_result"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING

    for payload in payloads:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
            payload=payload,
            method="POST",
            expected_status_codes=201,
        )
    # CLEANUP

    assert fail_log == ""


def test_POST_validation(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: load payloads
    TESTING: POST payloads for validation
    CLEANUP: None
    """

    fail_log = ""
    # SETUP

    endpoint_path = "validation"
    test_name = "Validate a user-defined process (graph)"

    directory_path = conformance_util.get_examples_path()
    examples_directory = "post_validation"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING

    for payload in payloads:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
            payload=payload,
            method="POST",
        )

    # CLEANUP

    assert fail_log == ""


def test_none_PUT_process_graphs_process_id(
    base_url: str, spec: Spec, bearer_token: str
):
    """
    SETUP: load empty payloads
    TESTING: PUT empty UDPs
    CLEANUP: None
    """
    fail_log = ""
    # SETUP

    endpoint_path = "process_graphs"

    test_name = "Store a user-defined process (NEGATIVE)"

    # TESTING

    id = str(uuid.uuid4())
    prepared_endpoint_path = f"{endpoint_path}/{id}"
    fail_log += conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=prepared_endpoint_path,
        test_name=f"{test_name} {id}",
        spec=spec,
        payload=None,
        bearer_token=bearer_token,
        method="PUT",
        expected_status_codes=range(400, 500),
    )

    # CLEANUP

    assert fail_log == ""


def test_negative_DELETE_process_graphs_process_id(
    base_url: str, spec: Spec, bearer_token: str
):
    """
    SETUP: None
    TESTING: try DELETE non-existant UDPs
    CLEANUP: None
    """
    fail_log = ""
    # SETUP

    endpoint = "process_graphs"
    prepared_endpoint_path = f"{endpoint}/thisiddoesnotexist"
    test_name = "Negative delete process graphs process id"

    # TESTING

    fail_log += conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=prepared_endpoint_path,
        test_name=test_name,
        spec=spec,
        bearer_token=bearer_token,
        method="DELETE",
        expected_status_codes=range(400, 501),
    )

    # CLEANUP
    assert fail_log == ""


def test_none_POST_jobs(base_url: str, spec: Spec, bearer_token: str):
    """
    setup: prepare empty payloads
    testing: test posting empty payloads endpoint
    cleanup: None
    """
    # SETUP
    endpoint_path = "jobs"
    test_name = "Creates a new batch processing task (NEGATIVE)"

    # TESTING
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=endpoint_path,
        test_name=test_name,
        spec=spec,
        bearer_token=bearer_token,
        payload=None,
        method="POST",
        expected_status_codes=range(400, 500),
    )

    # CLEANUP
    assert fail_log == ""


def test_none_PATCH_jobs_job_id(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, prepare payloads
    TESTING: PATCH jobs with empty payload
    CLEANUP: DELETE jobs
    """

    # SETUP
    fail_log = ""
    endpoint_path = "jobs"
    test_name = "Negative Modify a batch job"

    created_batch_job_ids = conformance_util.post_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    # TESTING
    for job_id in created_batch_job_ids:
        prepared_endpoint_path = f"{endpoint_path}/{job_id}"
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {job_id}",
            spec=spec,
            bearer_token=bearer_token,
            payload=None,
            method="PATCH",
            expected_status_codes=range(400, 500),
        )

    # CLEANUP
    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


def test_negative_DELETE_jobs_job_id(base_url: str, spec: Spec, bearer_token: str):
    """
    setup: None
    testing: Delete non-existent posted jobs
    cleanup: None
    """
    # SETUP
    endpoint_path = "jobs"
    test_name = "Delete specific batch job (NEGATIVE)"

    # TESTING
    prepared_endpoint_path = f"{endpoint_path}/thisiddoesnotexist"
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=prepared_endpoint_path,
        test_name=f"{test_name} for non-existant id",
        spec=spec,
        bearer_token=bearer_token,
        method="DELETE",
        expected_status_codes=range(400, 500),
    )

    # CLEANUP
    assert fail_log == ""


def test_negative_POST_jobs_job_id_results(
    base_url: str, spec: Spec, bearer_token: str
):
    """
    SETUP: None
    TESTING: start batch jobs that doesn't exist
    CLEANUP: None
    """
    # SETUP
    endpoint_path = "jobs"
    endpoint_path_extra = "results"
    test_name = "Start processing a batch job that doesn't exist"

    # TESTING
    prepared_endpoint_path = f"{endpoint_path}/thisiddoesnotexist/{endpoint_path_extra}"
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=prepared_endpoint_path,
        test_name=f"{test_name}",
        spec=spec,
        bearer_token=bearer_token,
        method="POST",
        expected_status_codes=range(400, 500),
    )

    # CLEANUP
    assert fail_log == ""


def test_negative_GET_jobs_job_id_results(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, START jobs (POST jobs/job_id/results), Wait for jobs to be finished
    TESTING: GET job results
    CLEANUP: DELETE Jobs
    """
    # SETUP
    endpoint_path = "jobs"
    endpoint_path_extra = "results"
    test_name = "Download results for a completed batch job that doesn't exist"

    # TESTING
    prepared_endpoint_path = f"{endpoint_path}/thisiddoesnotexist/{endpoint_path_extra}"
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=prepared_endpoint_path,
        test_name=f"{test_name}",
        spec=spec,
        bearer_token=bearer_token,
        method="GET",
        expected_status_codes=range(400, 500),
    )

    # CLEANUP
    assert fail_log == ""


def test_negative_DELETE_jobs_job_id_results(
    base_url: str, spec: Spec, bearer_token: str
):
    """
    SETUP:
    TESTING: DELETE job id results: Cancel processing jobs
    CLEANUP: None
    """
    # SETUP
    endpoint_path = "jobs"
    endpoint_path_extra = "results"
    test_name = "Cancel processing a batch job that doesn't exist"

    # TESTING
    prepared_endpoint_path = f"{endpoint_path}/thisiddoesnotexist/{endpoint_path_extra}"
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=prepared_endpoint_path,
        test_name=f"{test_name}",
        spec=spec,
        bearer_token=bearer_token,
        method="DELETE",
        expected_status_codes=range(400, 500),
    )

    # CLEANUP
    assert fail_log == ""


def test_negative_GET_jobs_job_id_logs(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: None
    TESTING: GET logs for batch jobs that don't exist
    CLEANUP:
    """
    # SETUP

    endpoint_path = "jobs"
    endpoint_path_extra = "logs"
    test_name = "Logs for a batch job"

    # TESTING

    prepared_endpoint_path = f"{endpoint_path}/thisiddoesnotexist/{endpoint_path_extra}"
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=prepared_endpoint_path,
        test_name=f"{test_name}",
        spec=spec,
        bearer_token=bearer_token,
        method="GET",
        expected_status_codes=range(400, 500),
    )
    # CLEANUP

    assert fail_log == ""


@pytest.mark.longrunning
def test_none_POST_result(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: gather payloads
    TESTING: POST empty payloads to result
    CLEANUP: None
    """
    # SETUP

    endpoint_path = "result"
    test_name = "Process and download data synchronously"

    # TESTING
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=endpoint_path,
        test_name=test_name,
        spec=spec,
        bearer_token=bearer_token,
        payload=None,
        method="POST",
        expected_status_codes=range(400, 500),
    )
    # CLEANUP

    assert fail_log == ""


def test_none_POST_validation(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: load empty payloads
    TESTING: POST empty payloads for validation
    CLEANUP: None
    """

    # SETUP
    endpoint_path = "validation"
    test_name = "Validate a user-defined process (graph)"

    # TESTING
    fail_log = conformance_util.test_endpoint(
        base_url=base_url,
        endpoint_path=endpoint_path,
        test_name=test_name,
        spec=spec,
        bearer_token=bearer_token,
        payload=None,
        method="POST",
        expected_status_codes=range(400, 500),
    )

    # CLEANUP
    assert fail_log == ""


def test_empty_PUT_process_graphs_process_id(
    base_url: str, spec: Spec, bearer_token: str
):
    """
    SETUP: load empty payloads
    TESTING: PUT empty UDPs
    CLEANUP: None
    """
    fail_log = ""
    # SETUP

    endpoint_path = "process_graphs"

    test_name = "Store a user-defined process (EMPTY)"

    directory_path = conformance_util.get_examples_path()
    examples_directory = "empty_payload"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING

    id = str(uuid.uuid4())
    prepared_endpoint_path = f"{endpoint_path}/{id}"

    for payload in payloads:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=prepared_endpoint_path,
            test_name=f"{test_name} {id}",
            spec=spec,
            payload=payload,
            bearer_token=bearer_token,
            method="PUT",
            expected_status_codes=range(400, 501),
        )

    # CLEANUP

    assert fail_log == ""


def test_empty_POST_jobs(base_url: str, spec: Spec, bearer_token: str):
    """
    setup: prepare empty payloads
    testing: test posting empty payloads endpoint
    cleanup: None
    """
    # SETUP
    fail_log = ""

    endpoint_path = "jobs"
    test_name = "Creates a new batch processing task (NEGATIVE)"
    directory_path = conformance_util.get_examples_path()
    examples_directory = "empty_payload"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}/"
    )

    # TESTING
    for payload in payloads:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
            payload=payload,
            method="POST",
            expected_status_codes=range(400, 501),
        )

    # CLEANUP
    assert fail_log == ""


def test_empty_PATCH_jobs_job_id(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: POST jobs, prepare payloads
    TESTING: PATCH jobs with empty payload
    CLEANUP: DELETE jobs
    """

    # SETUP
    fail_log = ""
    endpoint_path = "jobs"
    test_name = "Negative Modify a batch job"

    created_batch_job_ids = conformance_util.post_jobs(
        base_url=base_url, bearer_token=bearer_token
    )

    directory_path = conformance_util.get_examples_path()
    examples_directory = "empty_payload"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING
    for job_id in created_batch_job_ids:
        for payload in payloads:
            prepared_endpoint_path = f"{endpoint_path}/{job_id}"
            fail_log += conformance_util.test_endpoint(
                base_url=base_url,
                endpoint_path=prepared_endpoint_path,
                test_name=f"{test_name} {job_id}",
                spec=spec,
                bearer_token=bearer_token,
                payload=payload,
                method="PATCH",
                expected_status_codes=204,
            )

    # CLEANUP
    conformance_util.delete_id_resource(
        base_url=base_url,
        endpoint_path=endpoint_path,
        bearer_token=bearer_token,
        ids=created_batch_job_ids,
    )

    assert fail_log == ""


@pytest.mark.longrunning
def test_empty_POST_result(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: gather payloads
    TESTING: POST empty payloads to result
    CLEANUP: None
    """
    # SETUP

    endpoint_path = "result"
    test_name = "Process and download data synchronously"

    directory_path = conformance_util.get_examples_path()
    examples_directory = "empty_payload"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING
    for payload in payloads:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
            payload=payload,
            method="POST",
            expected_status_codes=range(400, 500),
        )
    # CLEANUP

    assert fail_log == ""


def test_empty_POST_validation(base_url: str, spec: Spec, bearer_token: str):
    """
    SETUP: load empty payloads
    TESTING: POST empty payloads for validation
    CLEANUP: None
    """

    # SETUP
    fail_log = ""

    endpoint_path = "validation"
    test_name = "Validate a user-defined process (graph)"

    directory_path = conformance_util.get_examples_path()
    examples_directory = "empty_payload"

    payloads = conformance_util.load_payloads_from_directory(
        directory_path=f"{directory_path}/{examples_directory}"
    )

    # TESTING
    for payload in payloads:
        fail_log += conformance_util.test_endpoint(
            base_url=base_url,
            endpoint_path=endpoint_path,
            test_name=test_name,
            spec=spec,
            bearer_token=bearer_token,
            payload=payload,
            method="POST",
            expected_status_codes=200,
        )

    # CLEANUP
    assert fail_log == ""


# endregion
