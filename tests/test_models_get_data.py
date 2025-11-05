import json

import pandas as pd
import pytest
import requests
import responses

from api_to_dataframe import DataFetchResult
from api_to_dataframe.controller.client_builder import ClientBuilder
from api_to_dataframe.models.get_data import GetData


def test_to_dataframe():
    """Raise ValueError when provided with empty input data."""

    with pytest.raises(ValueError):
        GetData.to_dataframe("")


@responses.activate
def test_to_emp_dataframe():
    """Propagate empty API payloads as dataframe errors."""

    endpoint = "https://api.exemplo.com"
    expected_response = []

    responses.add(responses.GET, endpoint, json=expected_response, status=200)

    client = ClientBuilder(endpoint=endpoint)
    response = client.get_api_data()

    assert isinstance(response, DataFetchResult)

    with pytest.raises(ValueError):
        GetData.to_dataframe(response.as_records())


@responses.activate
def test_valid_dataframe_conversion():
    """Test successful conversion of valid data to DataFrame"""
    # A estrutura do dict afeta como o pandas cria o DataFrame
    # Os dados precisam estar em uma lista para serem convertidos em linhas
    valid_data = [{"id": 1, "name": "Test"}, {"id": 2, "name": "Test2"}]
    df = GetData.to_dataframe(valid_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert "id" in df.columns
    assert "name" in df.columns
    assert df.iloc[0]["id"] == 1
    assert df.iloc[1]["name"] == "Test2"


@responses.activate
def test_nested_data_conversion():
    """Test conversion of nested data structures"""
    # Lista de dicionários é mais adequado para converter em DataFrame
    nested_data = [
        {"user": {"id": 1, "profile": {"name": "User1"}}},
        {"user": {"id": 2, "profile": {"name": "User2"}}}
    ]

    # Convert to string and back to dict to simulate JSON response
    json_str = json.dumps(nested_data)
    response_list = json.loads(json_str)

    df = GetData.to_dataframe(response_list)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 2
    # Verificar estrutura das colunas
    assert "user" in df.columns


@responses.activate
def test_http_error():
    """Ensure HTTP errors raise the expected exception type."""

    endpoint = "https://api.exemplo.com"
    expected_response = {}

    responses.add(responses.GET, endpoint, json=expected_response, status=400)

    with pytest.raises(requests.exceptions.HTTPError):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_http_error_with_custom_message():
    """Test HTTP error with custom error message in response"""
    endpoint = "https://api.exemplo.com/error"
    error_response = {"error": "Bad Request", "message": "Invalid parameters"}

    responses.add(
        responses.GET,
        endpoint,
        json=error_response,
        status=400
    )

    with pytest.raises(requests.exceptions.HTTPError):
        response = GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_timeout_error():
    """Surface timeout exceptions raised by the requests layer."""

    endpoint = "https://api.exemplo.com"

    responses.add(responses.GET, endpoint, body=requests.exceptions.Timeout())

    with pytest.raises(requests.exceptions.Timeout):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_request_exception():
    """Propagate generic request exceptions from the HTTP client."""

    endpoint = "https://api.exemplo.com"

    expected_response = {}

    responses.add(responses.GET, endpoint, json=expected_response, status=500)

    with pytest.raises(requests.exceptions.RequestException):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_headers_passed_correctly():
    """Test that headers are correctly passed to the request"""
    endpoint = "https://api.exemplo.com/headers"
    expected_response = {"success": True}
    custom_headers = {
        "Authorization": "Bearer test-token",
        "X-Custom-Header": "test-value",
        "Content-Type": "application/json"
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
        content_type="application/json"
    )

    response = GetData.get_response(
        endpoint=endpoint,
        headers=custom_headers,
        connection_timeout=10
    )

    assert response.status_code == 200
    assert response.json() == expected_response


@responses.activate
def test_query_params_are_forwarded():
    """Ensure query parameters are forwarded to the underlying request."""

    endpoint = "https://api.exemplo.com/params"
    expected_response = {"success": True}

    responses.add(
        responses.GET,
        endpoint,
        json=expected_response,
        match=[responses.matchers.query_param_matcher({"offset": "10", "limit": "5"})],
        status=200,
    )

    response = GetData.get_response(
        endpoint=endpoint,
        headers={},
        connection_timeout=10,
        params={"offset": 10, "limit": 5},
    )

    assert response.status_code == 200
    assert response.json() == expected_response
