import json
from typing import Any, Dict

import pandas as pd
import pytest
import requests
import responses
from responses import matchers

from api_to_dataframe.controller.client_builder import ClientBuilder
from api_to_dataframe.models.get_data import GetData


def test_to_dataframe_empty_payload():
    """Ensure converting an empty payload raises a ValueError."""

    with pytest.raises(ValueError):
        GetData.to_dataframe("")


@responses.activate
def test_to_dataframe_from_empty_response():
    """Validate that an empty response from the API raises a ValueError."""

    endpoint = "https://api.exemplo.com"
    expected_response: Dict[str, Any] = {}

    responses.add(responses.GET, endpoint, json=expected_response, status=200)

    client = ClientBuilder(endpoint=endpoint)
    response = client.get_api_data()

    with pytest.raises(ValueError):
        GetData.to_dataframe(response)


def test_valid_dataframe_conversion():
    """Test successful conversion of valid data to a DataFrame."""

    valid_data = [{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}]
    df = GetData.to_dataframe(valid_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "id" in df.columns
    assert "name" in df.columns
    assert df.iloc[0]["id"] == 1
    assert df.iloc[1]["name"] == "Test2"


def test_nested_data_conversion():
    """Test conversion of nested data structures."""

    nested_data = [
        {"user": {"id": 1, "profile": {"name": "User1"}}},
        {"user": {"id": 2, "profile": {"name": "User2"}}},
    ]

    json_str = json.dumps(nested_data)
    response_list = json.loads(json_str)

    df = GetData.to_dataframe(response_list)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 2
    assert "user" in df.columns


@pytest.mark.parametrize("method", ["GET", "POST", "PUT", "PATCH", "DELETE"])
@responses.activate
def test_http_methods_are_supported(method):
    """Ensure GetData can send requests using multiple HTTP methods."""

    endpoint = f"https://api.exemplo.com/{method.lower()}"
    expected_response = {"method": method}

    responses.add(getattr(responses, method), endpoint, json=expected_response, status=200)

    response = GetData.get_response(
        endpoint=endpoint,
        headers={},
        connection_timeout=10,
        method=method,
    )

    assert response.json() == expected_response


@responses.activate
def test_http_error():
    """Ensure HTTP errors raise the corresponding exception."""

    endpoint = "https://api.exemplo.com"
    expected_response = {}

    responses.add(responses.GET, endpoint, json=expected_response, status=400)

    with pytest.raises(requests.exceptions.HTTPError):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_http_error_with_custom_message():
    """Test HTTP error handling when a custom message is returned."""

    endpoint = "https://api.exemplo.com/error"
    error_response = {"error": "Bad Request", "message": "Invalid parameters"}

    responses.add(
        responses.GET,
        endpoint,
        json=error_response,
        status=400,
    )

    with pytest.raises(requests.exceptions.HTTPError):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_timeout_error():
    """Ensure timeout errors from requests are propagated."""

    endpoint = "https://api.exemplo.com"

    responses.add(responses.GET, endpoint, body=requests.exceptions.Timeout())

    with pytest.raises(requests.exceptions.Timeout):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_request_exception():
    """Ensure generic request exceptions are propagated."""

    endpoint = "https://api.exemplo.com"
    expected_response = {}

    responses.add(responses.GET, endpoint, json=expected_response, status=500)

    with pytest.raises(requests.exceptions.RequestException):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_headers_passed_correctly():
    """Verify that custom headers are forwarded to the HTTP request."""

    endpoint = "https://api.exemplo.com/headers"
    expected_response = {"success": True}
    custom_headers = {
        "Authorization": "Bearer test-token",
        "X-Custom-Header": "test-value",
        "Content-Type": "application/json",
    }

    def match_headers(request):
        for key, value in custom_headers.items():
            if request.headers.get(key) != value:
                return (400, {}, json.dumps({"error": "Header mismatch"}))
        return (200, {}, json.dumps(expected_response))

    responses.add_callback(
        responses.GET,
        endpoint,
        callback=match_headers,
        content_type="application/json",
    )

    response = GetData.get_response(
        endpoint=endpoint,
        headers=custom_headers,
        connection_timeout=10,
    )

    assert response.status_code == 200
    assert response.json() == expected_response


@responses.activate
def test_query_params_are_forwarded():
    """Verify that query parameters are forwarded to the request."""

    endpoint = "https://api.exemplo.com/query"
    params = {"page": "1", "size": "20"}
    expected_response = {"success": True}

    responses.add(
        responses.GET,
        endpoint,
        json=expected_response,
        match=[matchers.query_param_matcher(params)],
        status=200,
    )

    response = GetData.get_response(
        endpoint=endpoint,
        headers={},
        connection_timeout=10,
        params=params,
    )

    assert response.json() == expected_response


@responses.activate
def test_json_payload_is_sent():
    """Ensure JSON payloads are transmitted for request bodies."""

    endpoint = "https://api.exemplo.com/json"
    payload = {"name": "Jane"}
    expected_response = {"status": "ok"}

    def validate_json_payload(request):
        body_raw = request.body.decode("utf-8") if isinstance(request.body, bytes) else request.body
        body = json.loads(body_raw) if body_raw else {}
        if body != payload:
            return (400, {}, json.dumps({"error": "invalid"}))
        return (200, {}, json.dumps(expected_response))

    responses.add_callback(
        responses.POST,
        endpoint,
        callback=validate_json_payload,
        content_type="application/json",
    )

    response = GetData.get_response(
        endpoint=endpoint,
        headers={"Content-Type": "application/json"},
        connection_timeout=10,
        method="POST",
        json=payload,
    )

    assert response.json() == expected_response


@responses.activate
def test_form_payload_is_sent():
    """Ensure form payloads are transmitted correctly."""

    endpoint = "https://api.exemplo.com/form"
    payload = {"field": "value"}
    expected_response = {"status": "ok"}

    def validate_form_payload(request):
        body = (
            request.body.decode("utf-8")
            if isinstance(request.body, bytes)
            else (request.body or "")
        )
        if body != "field=value":
            return (400, {}, json.dumps({"error": "invalid"}))
        return (200, {}, json.dumps(expected_response))

    responses.add_callback(
        responses.POST,
        endpoint,
        callback=validate_form_payload,
        content_type="application/json",
    )

    response = GetData.get_response(
        endpoint=endpoint,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        connection_timeout=10,
        method="POST",
        data=payload,
    )

    assert response.json() == expected_response


def test_custom_session_is_used():
    """Ensure a custom session object is used for the request."""

    class DummySession:
        """Dummy session collecting the last request call."""

        def __init__(self):
            self.called_with = None

        def request(self, **kwargs):
            self.called_with = kwargs

            class DummyResponse:
                """Simple response mimicking the requests interface."""

                def __init__(self):
                    self._json = {"status": "dummy"}

                def raise_for_status(self):
                    return None

                def json(self):
                    return self._json

            return DummyResponse()

    session = DummySession()

    response = GetData.get_response(
        endpoint="https://api.exemplo.com/session",
        headers={},
        connection_timeout=10,
        session=session,
    )

    assert session.called_with["method"] == "GET"
    assert response.json()["status"] == "dummy"


def test_invalid_method_raises_value_error():
    """Ensure invalid HTTP method values raise ValueError."""

    with pytest.raises(ValueError):
        GetData.get_response(
            endpoint="http://example.com",
            headers={},
            connection_timeout=10,
            method="",
        )
