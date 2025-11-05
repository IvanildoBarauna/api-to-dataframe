"""Tests for the pagination helpers integrated with ClientBuilder."""

import pytest
import responses

from api_to_dataframe import ClientBuilder, PaginationStrategy


@responses.activate
def test_offset_limit_pagination_collects_all_pages():
    """Aggregate multiple offset/limit pages into a single result."""

    endpoint = "https://api.example.com/resources"
    first_page = {"items": [{"id": 1}, {"id": 2}]}
    second_page = {"items": [{"id": 3}]}

    responses.add(
        responses.GET,
        endpoint,
        json=first_page,
        match=[responses.matchers.query_param_matcher({"offset": "0", "limit": "2"})],
        status=200,
    )
    responses.add(
        responses.GET,
        endpoint,
        json=second_page,
        match=[responses.matchers.query_param_matcher({"offset": "2", "limit": "2"})],
        status=200,
    )

    client = ClientBuilder(endpoint=endpoint)
    client.with_pagination(
        PaginationStrategy.OFFSET_LIMIT,
        limit=2,
        results_key="items",
    )

    result = client.get_api_data()

    assert result.metadata["strategy"] == PaginationStrategy.OFFSET_LIMIT.value
    assert result.metadata["pages"] == 2
    assert result.metadata["last_params"] == {"offset": 2, "limit": 2}
    assert [item["id"] for item in result.records] == [1, 2, 3]


@responses.activate
def test_page_pagination_stops_on_empty_page():
    """Stop requesting new pages once an empty list is returned."""

    endpoint = "https://api.example.com/paged"
    second_page = {"results": [{"page": 2}]}
    empty_page = {"results": []}

    responses.add(
        responses.GET,
        endpoint,
        json=second_page,
        match=[responses.matchers.query_param_matcher({"page": "2"})],
        status=200,
    )
    responses.add(
        responses.GET,
        endpoint,
        json=empty_page,
        match=[responses.matchers.query_param_matcher({"page": "3"})],
        status=200,
    )

    client = ClientBuilder(endpoint=endpoint)
    client.with_pagination(
        PaginationStrategy.PAGE,
        start_page=2,
        results_key="results",
    )

    result = client.get_api_data()

    assert result.metadata["pages"] == 2
    assert result.records == [{"page": 2}]
    assert result.metadata["last_params"] == {"page": 3}


@responses.activate
def test_cursor_pagination_tracks_cursor_value():
    """Cursor pagination returns combined records and cursor metadata."""

    endpoint = "https://api.example.com/cursor"
    first = {"data": [{"id": "a"}], "next_cursor": "abc"}
    second = {"data": [{"id": "b"}], "next_cursor": None}

    responses.add(
        responses.GET,
        endpoint,
        json=first,
        status=200,
    )
    responses.add(
        responses.GET,
        endpoint,
        json=second,
        match=[responses.matchers.query_param_matcher({"cursor": "abc"})],
        status=200,
    )

    client = ClientBuilder(endpoint=endpoint)
    client.with_pagination(
        PaginationStrategy.CURSOR,
        results_key="data",
        next_cursor_key="next_cursor",
    )

    result = client.get_api_data()

    assert result.metadata["pages"] == 2
    assert result.metadata["last_cursor"] is None
    assert [item["id"] for item in result.records] == ["a", "b"]


def test_with_pagination_invalid_offset_limit_arguments():
    """Invalid limit values should raise a ValueError."""

    client = ClientBuilder(endpoint="https://api.example.com/resources")

    with pytest.raises(ValueError):
        client.with_pagination(PaginationStrategy.OFFSET_LIMIT, limit=0)


def test_with_pagination_invalid_page_arguments():
    """Page strategy validates the starting page value."""

    client = ClientBuilder(endpoint="https://api.example.com/resources")

    with pytest.raises(ValueError):
        client.with_pagination(PaginationStrategy.PAGE, start_page=0)
