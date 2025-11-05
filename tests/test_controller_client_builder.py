import pytest
import pandas as pd
import responses

from api_to_dataframe import ClientBuilder, RetryStrategies


@pytest.fixture()
def client_setup():
    """Create a client with a mocked API endpoint."""

    endpoint = "https://economia.awesomeapi.com.br/last/USD-BRL"
    mocked_payload = {"USDBRL": {"code": "USD", "codein": "BRL", "bid": "5.0"}}
    responses_mock = responses.RequestsMock(assert_all_requests_are_fired=False)
    responses_mock.start()
    responses_mock.add(responses.GET, endpoint, json=mocked_payload, status=200)

    client = ClientBuilder(endpoint=endpoint)
    yield client

    responses_mock.stop()
    responses_mock.reset()


@pytest.fixture()
def response_setup():
    """Provide a mocked API response as a dictionary."""

    endpoint = "https://economia.awesomeapi.com.br/last/USD-BRL"
    mocked_payload = {"USDBRL": {"code": "USD", "codein": "BRL", "bid": "5.0"}}
    responses_mock = responses.RequestsMock(assert_all_requests_are_fired=False)
    responses_mock.start()
    responses_mock.add(responses.GET, endpoint, json=mocked_payload, status=200)

    new_client = ClientBuilder(endpoint=endpoint)
    response = new_client.get_api_data()

    responses_mock.stop()
    responses_mock.reset()

    return response


def test_constructor_raises():
    """Ensure constructor validates required arguments."""
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
    """Verify constructor assigns provided endpoint."""
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


def test_response_to_json(client_setup):  # pylint: disable=redefined-outer-name
    """Validate the client converts the mocked response to a dict."""
    new_client = client_setup
    response = new_client.get_api_data()  # pylint: disable=protected-access
    assert isinstance(response, dict)


def test_to_dataframe(response_setup):  # pylint: disable=redefined-outer-name
    """Confirm the API response can be converted into a DataFrame."""
    df = ClientBuilder.api_to_dataframe(response_setup)
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

    assert response == expected_data
    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == endpoint
