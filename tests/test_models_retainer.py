import time
import requests
import pytest

from api_to_dataframe import ClientBuilder, RetryStrategies


def test_linear_strategy():
    endpoint = "https://api-to-dataframe/"
    max_retries = 2
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.LINEAR_RETRY_STRATEGY,
        retries=max_retries,
        initial_delay=1,
        connection_timeout=1,
    )

    retry_number = 0

    while retry_number < max_retries:
        start = time.time()
        try:
            client.get_api_data()
        except requests.exceptions.RequestException:
            end = time.time()
            assert end - start >= client.delay
            retry_number += 1

    assert retry_number == max_retries


def test_no_retry_strategy():
    endpoint = "https://api-to-dataframe/"
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.NO_RETRY_STRATEGY,
    )

    with pytest.raises(requests.exceptions.RequestException):
        client.get_api_data()


def test_exponential_strategy():
    endpoint = "https://api-to-dataframe/"
    max_retries = 2
    client = ClientBuilder(
        endpoint=endpoint,
        retry_strategy=RetryStrategies.EXPONENTIAL_RETRY_STRATEGY,
        retries=max_retries,
        initial_delay=1,
        connection_timeout=1,
    )

    retry_number = 0

    while retry_number < max_retries:
        start = time.time()
        try:
            client.get_api_data()
        except requests.exceptions.RequestException:
            end = time.time()
            assert end - start >= client.delay * retry_number
            retry_number += 1

    assert retry_number == max_retries
