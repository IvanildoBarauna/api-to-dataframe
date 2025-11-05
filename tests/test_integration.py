"""Integration tests covering end-to-end flows."""

import pandas as pd
import responses

from api_to_dataframe import ClientBuilder, RetryStrategies


@responses.activate
def test_full_flow_simple_api():
    """Test the full flow from API request to DataFrame conversion with a simple API response."""

    endpoint = "https://api.example.com/data"
    api_response = [
        {"id": 1, "name": "Item 1", "price": 10.99},
        {"id": 2, "name": "Item 2", "price": 20.50},
        {"id": 3, "name": "Item 3", "price": 5.25},
    ]

    responses.add(responses.GET, endpoint, json=api_response, status=200)

    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=3,
        connection_timeout=5,
    )

    response_data = client.get_api_data()
    assert response_data.metadata["strategy"] == "single"

    df = client.api_to_dataframe(response_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 3
    assert "id" in df.columns
    assert "name" in df.columns
    assert "price" in df.columns
    assert df.iloc[0]["name"] == "Item 1"
    assert df.iloc[1]["price"] == 20.50
    assert df.iloc[2]["id"] == 3


@responses.activate
def test_full_flow_with_retry():
    """Test the full flow with a failed request that succeeds after retry."""

    endpoint = "https://api.example.com/data/retry"
    api_response = [{"id": 1, "value": "Success after retry"}]

    responses.add(responses.GET, endpoint, status=500, json={"error": "Server Error"})
    responses.add(responses.GET, endpoint, json=api_response, status=200)

    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=3,
        initial_delay=1,
        connection_timeout=5,
    )

    response_data = client.get_api_data()
    assert response_data.metadata["strategy"] == "single"

    df = client.api_to_dataframe(response_data)

    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "id" in df.columns
    assert "value" in df.columns
    assert df.iloc[0]["id"] == 1
    assert df.iloc[0]["value"] == "Success after retry"

    assert len(responses.calls) == 2
