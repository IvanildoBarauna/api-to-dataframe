"""Tests for the GetData model utilities."""

import json
from typing import Any

import pandas as pd
import pytest
import requests
import responses

from api_to_dataframe.controller.client_builder import ClientBuilder
from api_to_dataframe.models.get_data import GetData


def test_to_dataframe_rejects_empty_string() -> None:
    """Ensure a string payload without data raises a ValueError."""

    with pytest.raises(ValueError):
        GetData.to_dataframe("")


def test_to_dataframe_rejects_empty_list_by_default() -> None:
    """Validate that an empty iterable raises a ValueError when using default settings."""

    with pytest.raises(ValueError):
        GetData.to_dataframe([])


def test_to_dataframe_allows_ignore_errors_for_empty_payload() -> None:
    """Confirm that ignoring errors returns an empty DataFrame instead of raising."""

    dataframe = GetData.to_dataframe([], errors="ignore")

    assert isinstance(dataframe, pd.DataFrame)
    assert dataframe.empty


def test_to_dataframe_flattens_nested_structure() -> None:
    """Check that nested dictionaries are flattened using pandas.json_normalize."""

    payload = [
        {"user": {"id": 1, "profile": {"name": "User1", "active": True}}},
        {"user": {"id": 2, "profile": {"name": "User2", "active": False}}},
    ]

    dataframe = GetData.to_dataframe(payload, max_level=1)

    assert list(dataframe.columns) == ["user.id", "user.profile"]
    assert dataframe.iloc[0]["user.id"] == 1
    assert dataframe.iloc[1]["user.profile"].get("name") == "User2"


def test_to_dataframe_with_custom_record_path_and_meta() -> None:
    """Ensure record_path and meta arguments are forwarded to pandas.json_normalize."""

    payload = {
        "metadata": {"batch": "A", "source": "unit-test"},
        "items": [
            {"id": 1, "value": "alpha"},
            {"id": 2, "value": "beta"},
        ],
    }

    dataframe = GetData.to_dataframe(
        payload,
        record_path="items",
        meta=["metadata"],
    )

    assert "metadata" in dataframe.columns
    assert dataframe.iloc[0]["metadata"]["batch"] == "A"
    assert dataframe.iloc[1]["value"] == "beta"


@responses.activate
def test_to_dataframe_handles_nested_list_via_record_path() -> None:
    """Validate normalization when the response is retrieved from the HTTP client."""

    endpoint = "https://api.example.com/nested"
    payload = {
        "meta": {"page": 1},
        "results": [
            {"id": 1, "attributes": {"name": "Item1"}},
            {"id": 2, "attributes": {"name": "Item2"}},
        ],
    }

    responses.add(responses.GET, endpoint, json=payload, status=200)

    client = ClientBuilder(endpoint=endpoint)
    response = client.get_api_data()

    dataframe = client.api_to_dataframe(
        response,
        record_path="results",
        meta=[["meta", "page"]],
    )

    assert list(dataframe.columns) == ["id", "attributes.name", "meta.page"]
    assert dataframe.iloc[0]["meta.page"] == 1
    assert dataframe.iloc[1]["attributes.name"] == "Item2"


@responses.activate
def test_to_dataframe_supports_transformer_before_normalization() -> None:
    """Check that ClientBuilder applies a transformer before delegating to GetData."""

    endpoint = "https://api.example.com/items"
    payload = {"data": [{"id": 1}, {"id": 2}]}

    responses.add(responses.GET, endpoint, json=payload, status=200)

    def transformer(raw: Any) -> Any:
        return raw["data"]

    client = ClientBuilder(endpoint=endpoint, transformer=transformer)
    response = client.get_api_data()

    dataframe = client.api_to_dataframe(response)

    assert isinstance(dataframe, pd.DataFrame)
    assert list(dataframe["id"]) == [1, 2]


@responses.activate
def test_http_error() -> None:
    """Ensure HTTP errors are propagated when the API returns a bad status."""

    endpoint = "https://api.exemplo.com"
    responses.add(responses.GET, endpoint, json={}, status=400)

    with pytest.raises(requests.exceptions.HTTPError):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_timeout_error() -> None:
    """Ensure timeout exceptions are surfaced to callers."""

    endpoint = "https://api.exemplo.com"

    responses.add(responses.GET, endpoint, body=requests.exceptions.Timeout())

    with pytest.raises(requests.exceptions.Timeout):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_request_exception() -> None:
    """Ensure generic request exceptions are raised when appropriate."""

    endpoint = "https://api.exemplo.com"

    responses.add(responses.GET, endpoint, json={}, status=500)

    with pytest.raises(requests.exceptions.RequestException):
        GetData.get_response(endpoint=endpoint, headers={}, connection_timeout=10)


@responses.activate
def test_headers_passed_correctly() -> None:
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
