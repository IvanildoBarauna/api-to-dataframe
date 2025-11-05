import pytest
import pandas as pd
import responses

from api_to_dataframe import ClientBuilder, RetryStrategies


@pytest.fixture()
def client_setup():
    """Create a default ClientBuilder instance for tests."""
    new_client = ClientBuilder(
        endpoint="https://economia.awesomeapi.com.br/last/USD-BRL"
    )
    return new_client


def test_constructor_raises():
    """Ensure constructor validations raise errors for invalid inputs."""
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
    """Ensure constructor stores the provided endpoint value."""
    expected_result = "https://economia.awesomeapi.com.br/last/USD-BRL"
    new_client = client_setup
    assert new_client.endpoint == expected_result


def test_constructor_with_headers():
    """Test ClientBuilder with custom headers."""
    custom_headers = {"Authorization": "Bearer token123", "Content-Type": "application/json"}
    client = ClientBuilder(
        endpoint="https://economia.awesomeapi.com.br/last/USD-BRL",
        headers=custom_headers
    )
    assert client.headers == custom_headers


def test_constructor_with_retry_strategy():
    """Test ClientBuilder with different retry strategies."""
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
    """Ensure API responses are converted to JSON objects."""
    new_client = client_setup
    expected_response = {"key": "value"}

    responses.add(
        responses.GET,
        new_client.endpoint,
        json=expected_response,
        status=200,
    )

    response = new_client.get_api_data()  # pylint: disable=protected-access
    assert isinstance(response, dict)
    assert response == expected_response


def test_to_dataframe():
    """Ensure responses can be converted into DataFrames."""
    sample_response = [{"currency": "USD", "bid": "5.0"}]
    df = ClientBuilder.api_to_dataframe(sample_response)
    assert isinstance(df, pd.DataFrame)


@responses.activate
def test_get_api_data_with_mocked_response():
    """Test get_api_data with mocked API response."""
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


def test_with_method_configures_request_method():
    """Ensure with_method configures the HTTP method for requests."""

    client = ClientBuilder(endpoint="https://api.test.com").with_method("post")
    assert client._method == "POST"  # pylint: disable=protected-access


def test_with_params_validates_input_type():
    """Ensure with_params only accepts dictionaries."""

    client = ClientBuilder(endpoint="https://api.test.com")
    assert client.with_params({"page": 1}) is client

    with pytest.raises(ValueError):
        client.with_params([("page", 1)])


def test_with_payload_replaces_existing_payload():
    """Ensure with_payload stores json, data and file payloads."""

    client = ClientBuilder(endpoint="https://api.test.com")
    client.with_payload(json={"name": "Jane"}, data=None)

    assert client._json_payload == {"name": "Jane"}  # pylint: disable=protected-access
    assert client._data_payload is None  # pylint: disable=protected-access


def test_with_session_validates_interface():
    """Ensure with_session requires an object exposing request."""

    client = ClientBuilder(endpoint="https://api.test.com")

    class DummySession:
        """Expose a request method to mimic a real session."""

        def request(self, **kwargs):  # pragma: no cover - dummy implementation
            return kwargs

    session = DummySession()
    assert client.with_session(session) is client

    with pytest.raises(ValueError):
        client.with_session(object())


@responses.activate
def test_fluent_configuration_executes_request():
    """Ensure fluent configuration works when executing requests."""

    endpoint = "https://api.test.com/submit"
    payload = {"name": "John"}
    expected_response = {"status": "created"}

    responses.add(
        responses.POST,
        endpoint,
        json=expected_response,
        status=201,
    )

    client = (
        ClientBuilder(endpoint=endpoint)
        .with_method("POST")
        .with_payload(json=payload)
        .with_params({"verbose": "true"})
    )

    response = client.get_api_data()

    assert response == expected_response
    assert responses.calls[0].request.method == "POST"
    assert "verbose=true" in responses.calls[0].request.url
