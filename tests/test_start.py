import json
import os

import pytest
import responses

from action.start import start


@pytest.fixture()
def env():
    os.environ["INPUT_REPOSITORY"] = "Org/exampleRepo"
    os.environ["INPUT_GITHUB_PAT"] = "666"
    os.environ["INPUT_EVENT"] = "order"
    os.environ["PAYLOAD_AUTHOR"] = "john.doe"
    return "https://api.github.com/repos/Org/exampleRepo/dispatches"


@responses.activate
def test_request_ok(env):
    responses.add(responses.POST, env)
    start()
    assert responses.assert_call_count(env, 1)


@responses.activate
def test_headers_ok(env):
    responses.add(responses.POST, env)
    start()
    assert responses.calls[0].request.headers["Authorization"] == "token 666"


@responses.activate
def test_payload_ok(env):
    responses.add(responses.POST, env)
    start()
    body = responses.calls[0].request.body
    assert json.loads(body)["client_payload"]["AUTHOR"] == "john.doe"


@responses.activate
def test_event_type_ok(env):
    responses.add(responses.POST, env)
    start()
    body = responses.calls[0].request.body
    assert json.loads(body)["event_type"] == "order"


@responses.activate
def test_request_error_with_message(env):
    responses.add(responses.POST, env, status=400, json={"message": "ops"})
    with pytest.raises(SystemExit):
        start()


@responses.activate
def test_request_error_without_message(env):
    responses.add(responses.POST, env, status=400)
    with pytest.raises(SystemExit):
        start()
