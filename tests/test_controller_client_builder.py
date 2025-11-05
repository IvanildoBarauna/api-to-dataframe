import pytest
import pandas as pd
import responses

from api_to_dataframe import ClientBuilder, DataFetchResult, RetryStrategies


@pytest.fixture()
def client_setup():
    """Create a basic ClientBuilder instance for tests."""

    new_client = ClientBuilder(endpoint="https://economia.awesomeapi.com.br/last/USD-BRL")
    return new_client


def test_constructor_raises():
    """Validate constructor argument validation logic."""

    with pytest.raises(ValueError):
        ClientBuilder(endpoint="")

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", retries=-1
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", initial_delay=-1
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            connection_timeout=-1,
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", retries=""
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL", initial_delay=""
        )

    with pytest.raises(ValueError):
        ClientBuilder(
            endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
            connection_timeout="",
        )


def test_constructor_with_param(client_setup):  # pylint: disable=redefined-outer-name
    """Ensure constructor stores the provided endpoint."""

    expected_result = "https://economia.awesomeapi.com.br/last/USD-BRL"
    new_client = client_setup
    assert new_client.endpoint == expected_result


def test_constructor_with_headers():
    """Test ClientBuilder with custom headers"""
    custom_headers = {"Authorization": "Bearer token123", "Content-Type": "application/json"}
    client = ClientBuilder(
        endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
        headers=custom_headers
    )
    assert client.headers == custom_headers


def test_constructor_with_retry_strategy():
    """Test ClientBuilder with different retry strategies"""
    client = ClientBuilder(
        endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=5,
        initial_delay=2
    )
    assert client.retry_strategy == RetryStrategies.LINEAR_RETRY_STRATEGY
    assert client.retries == 5
    assert client.delay == 2


@responses.activate
def test_response_to_json(client_setup):  # pylint: disable=redefined-outer-name
    """Ensure get_api_data returns a DataFetchResult."""

    new_client = client_setup
    responses.add(
        responses.GET,
        new_client.endpoint,
        json={"mocked": True},
        status=200,
    )
    response = new_client.get_api_data()
    assert isinstance(response, DataFetchResult)
    assert response.metadata["strategy"] == "single"


@responses.activate
def test_to_dataframe():
    """Convert aggregated API data to DataFrame."""

    client = ClientBuilder(endpoint="https://economia.awesomeapi.com.br/last/USD-BRL")
    responses.add(
        responses.GET,
        client.endpoint,
        json=[{"value": 1}],
        status=200,
    )
    response = client.get_api_data()
    df = ClientBuilder.api_to_dataframe(response)
    assert isinstance(df, pd.DataFrame)


@responses.activate
def test_get_api_data_with_mocked_response():
    """Test get_api_data with mocked API response"""
    endpoint = "https://api.test.com/data"
    expected_data = {"key": "value", "nested": {"id": 123}}

    # Mock the API response
    responses.add(
        responses.GET,
        endpoint,
        json=expected_data,
        status=200
    )

    client = ClientBuilder(endpoint=endpoint)
    response = client.get_api_data()

    assert isinstance(response, DataFetchResult)
    assert response.as_records() == [expected_data]
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == endpoint


@responses.activate
def test_with_pagination_invalid_strategy_value():
    """Raise ValueError when configuring an unknown pagination strategy."""

    client = ClientBuilder(endpoint="https://api.test.com/data")

    with pytest.raises(ValueError):
        client.with_pagination("unknown")
