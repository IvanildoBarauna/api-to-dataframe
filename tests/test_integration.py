import pytest
import responses
import pandas as pd

from api_to_dataframe import ClientBuilder, RetryStrategies


@responses.activate
def test_full_flow_simple_api():
    """Test the full flow from API request to DataFrame conversion with a simple API response"""
    # Setup mock API
    endpoint = "https://api.example.com/data"
    # Modificado para retornar lista diretamente, não encapsulado em dicionário
    api_response = [
        {"id": 1, "name": "Item 1", "price": 10.99},
        {"id": 2, "name": "Item 2", "price": 20.50},
        {"id": 3, "name": "Item 3", "price": 5.25},
    ]

    responses.add(responses.GET, endpoint, json=api_response, status=200)

    # Create client and fetch data
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=3,
        connection_timeout=5,
    )

    # Get API data
    response_data = client.get_api_data()

    # Convert to DataFrame
    df = client.api_to_dataframe(response_data)

    # Assertions
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
    """Test the full flow with a failed request that succeeds after retry"""
    endpoint = "https://api.example.com/data/retry"
    # Modificado para lista direta, similar ao teste anterior
    api_response = [{"id": 1, "value": "Success after retry"}]

    # Add a failing response first
    responses.add(responses.GET, endpoint, status=500, json={"error": "Server Error"})

    # Add a successful response for subsequent requests
    responses.add(responses.GET, endpoint, json=api_response, status=200)

    # Create client with retry strategy
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=3,
        initial_delay=1,
        connection_timeout=5,
    )

    # Get API data - should succeed after retry
    response_data = client.get_api_data()

    # Convert to DataFrame
    df = client.api_to_dataframe(response_data)

    # Assertions
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 1
    assert "id" in df.columns
    assert "value" in df.columns
    assert df.iloc[0]["id"] == 1
    assert df.iloc[0]["value"] == "Success after retry"

    # Verify we had 2 calls (first failed, second succeeded)
    assert len(responses.calls) == 2
