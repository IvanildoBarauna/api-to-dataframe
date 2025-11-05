import logging
import requests
import pytest

from api_to_dataframe import ClientBuilder, RetryStrategies
from api_to_dataframe.utils import Constants


def _raise_request_exception(*args, **kwargs):
    raise requests.exceptions.RequestException("boom")


def test_linear_strategy(monkeypatch):
    """Ensure the linear strategy sleeps for a constant interval between retries."""

    monkeypatch.setattr(
        "src.api_to_dataframe.models.get_data.requests.get",
        _raise_request_exception,
    )
    sleep_calls = []

    def fake_sleep(delay):
        sleep_calls.append(delay)

    monkeypatch.setattr("src.api_to_dataframe.models.retainer.time.sleep", fake_sleep)

    client = ClientBuilder(
        endpoint="https://api-to-dataframe/",
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=2,
        initial_delay=1,
        connection_timeout=1,
    )

    with pytest.raises(requests.exceptions.RequestException):
        client.get_api_data()

    assert sleep_calls == [1, 1]


def test_no_retry_strategy(monkeypatch):
    """Validate that no retry strategy raises immediately without sleeping."""

    monkeypatch.setattr(
        "src.api_to_dataframe.models.get_data.requests.get",
        _raise_request_exception,
    )
    sleep_calls = []

    def fake_sleep(delay):
        sleep_calls.append(delay)

    monkeypatch.setattr("src.api_to_dataframe.models.retainer.time.sleep", fake_sleep)

    client = ClientBuilder(
        endpoint="https://api-to-dataframe/",
        retry_strategy=RetryStrategies.NO_RETRY_STRATEGY,
    )

    with pytest.raises(requests.exceptions.RequestException):
        client.get_api_data()

    assert sleep_calls == []


def test_exponential_strategy(monkeypatch):
    """Ensure the exponential strategy multiplies the delay by the retry attempt."""

    monkeypatch.setattr(
        "src.api_to_dataframe.models.get_data.requests.get",
        _raise_request_exception,
    )
    sleep_calls = []

    def fake_sleep(delay):
        sleep_calls.append(delay)

    monkeypatch.setattr("src.api_to_dataframe.models.retainer.time.sleep", fake_sleep)

    client = ClientBuilder(
        endpoint="https://api-to-dataframe/",
        retry_strategy=RetryStrategies.EXPONENTIAL_RETRY_STRATEGY,
        retries=3,
        initial_delay=1,
        connection_timeout=1,
    )

    with pytest.raises(requests.exceptions.RequestException):
        client.get_api_data()

    assert sleep_calls == [1, 2, 3]


def test_global_retry_cap_applied(caplog):
    """Check that the global retry cap is enforced and a warning is logged when clamped."""

    caplog.set_level(logging.WARNING)

    client = ClientBuilder(
        endpoint="https://api-to-dataframe/",
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=Constants.MAX_OF_RETRIES + 2,
        initial_delay=1,
        connection_timeout=1,
    )

    assert client.retries == Constants.MAX_OF_RETRIES
    assert "Clamping" in caplog.text


def test_exponential_strategy_uses_jitter(monkeypatch):
    """Verify that exponential retries add the configured jitter to the sleep duration."""

    monkeypatch.setattr(
        "src.api_to_dataframe.models.get_data.requests.get",
        _raise_request_exception,
    )
    sleep_calls = []

    def fake_sleep(delay):
        sleep_calls.append(delay)

    monkeypatch.setattr("src.api_to_dataframe.models.retainer.time.sleep", fake_sleep)

    jitter_values = [0.5, 0.25]

    def fake_uniform(_, __):
        return jitter_values.pop(0)

    monkeypatch.setattr(
        "src.api_to_dataframe.models.retainer.random.uniform",
        fake_uniform,
    )

    client = ClientBuilder(
        endpoint="https://api-to-dataframe/",
        retry_strategy=RetryStrategies.EXPONENTIAL_RETRY_STRATEGY,
        retries=2,
        initial_delay=1,
        connection_timeout=1,
        jitter=1.0,
    )

    with pytest.raises(requests.exceptions.RequestException):
        client.get_api_data()

    assert sleep_calls == [1.5, 2.25]
