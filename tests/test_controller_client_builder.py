import pytest
import pandas as pd
import responses

from api_to_dataframe import ClientBuilder, RetryStrategies
from api_to_dataframe.models.auth import ApiKeyAuth


@pytest.fixture()
def client_setup():
    new_client = ClientBuilder(
        endpoint="https://economia.awesomeapi.com.br/last/USD-BRL"
    )
    return new_client


def test_constructor_raises():
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
    """Test JSON response retrieval using a mocked HTTP endpoint."""
    expected_payload = {"rate": 5.2}
    responses.add(
        responses.GET,
        client_setup.endpoint,
        json=expected_payload,
        status=200,
    )

    new_client = client_setup
    response = new_client.get_api_data()  # pylint: disable=protected-access

    assert response == expected_payload


@responses.activate
def test_to_dataframe(client_setup):  # pylint: disable=redefined-outer-name
    """Test DataFrame conversion using mocked API data."""
    expected_payload = {"id": [1, 2], "value": ["a", "b"]}
    responses.add(
        responses.GET,
        client_setup.endpoint,
        json=expected_payload,
        status=200,
    )

    response_data = client_setup.get_api_data()
    df = ClientBuilder.api_to_dataframe(response_data)

    assert isinstance(df, pd.DataFrame)
    assert not df.empty


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

    assert response == expected_data
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == endpoint


@responses.activate
def test_client_builder_with_auth_headers():
    """Ensure ClientBuilder augments request headers using the auth provider."""
    endpoint = "https://api.test.com/data"
    responses.add(responses.GET, endpoint, json={"status": "ok"}, status=200)

    client = ClientBuilder(endpoint=endpoint, headers={"Accept": "application/json"})
    client.with_auth(ApiKeyAuth("X-Api-Key", "secret"))

    payload = client.get_api_data()

    sent_headers = responses.calls[0].request.headers
    assert payload == {"status": "ok"}
    assert sent_headers["X-Api-Key"] == "secret"
    assert sent_headers["Accept"] == "application/json"
