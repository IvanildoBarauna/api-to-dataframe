# API to DataFrame

Fetch JSON from any HTTP API and turn it into a pandas DataFrame in two calls — with optional retry strategies.

[![PyPI - Version](https://img.shields.io/pypi/v/api-to-dataframe?style=for-the-badge&logo=pypi)](https://pypi.org/project/api-to-dataframe/#history)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/api-to-dataframe?style=for-the-badge&logo=pypi)](https://pypi.org/project/api-to-dataframe/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/api-to-dataframe?style=for-the-badge&logo=python)](https://pypi.org/project/api-to-dataframe/)
[![CI](https://img.shields.io/github/actions/workflow/status/ivanildobarauna-dev/api-to-dataframe/CI.yaml?style=for-the-badge&logo=githubactions&label=CI)](https://github.com/ivanildobarauna-dev/api-to-dataframe/actions/workflows/CI.yaml)
[![Codecov](https://img.shields.io/codecov/c/github/ivanildobarauna-dev/api-to-dataframe?style=for-the-badge&logo=codecov)](https://app.codecov.io/gh/ivanildobarauna-dev/api-to-dataframe)

## Install

```sh
pip install api-to-dataframe
# or
poetry add api-to-dataframe
```

Requires Python 3.10+.

## Quick start

```python
from api_to_dataframe import ClientBuilder, RetryStrategies

client = ClientBuilder(endpoint="https://api.example.com/items")
data = client.get_api_data()
df = client.api_to_dataframe(data)
```

`api_to_dataframe` expects the response to be a list of dicts. An empty result raises `ValueError`.

## Configuration

```python
client = ClientBuilder(
    endpoint="https://api.example.com/items",
    headers={"Authorization": "Bearer ..."},
    retry_strategy=RetryStrategies.EXPONENTIAL_RETRY_STRATEGY,
    retries=5,
    initial_delay=2,
    connection_timeout=10,
)
```

| Parameter            | Default              | Description                                         |
| -------------------- | -------------------- | --------------------------------------------------- |
| `endpoint`           | — (required)         | Target URL.                                         |
| `headers`            | `None`               | Request headers.                                    |
| `retry_strategy`     | `NO_RETRY_STRATEGY`  | See strategies below.                               |
| `retries`            | `3`                  | Max attempts. Hard-capped at 5.                     |
| `initial_delay`      | `1`                  | Base delay in seconds between retries.              |
| `connection_timeout` | `10`                 | Per-request timeout in seconds.                     |

## Retry strategies

- `NO_RETRY_STRATEGY` — fail fast on the first error.
- `LINEAR_RETRY_STRATEGY` — wait `initial_delay` seconds before each retry.
- `EXPONENTIAL_RETRY_STRATEGY` — wait `initial_delay * retry_number` seconds before each retry.

Retries are capped at 5 regardless of the `retries` value.

## Links

- [PyPI](https://pypi.org/project/api-to-dataframe/)
- [Example notebook](https://github.com/IvanildoBarauna/api-to-dataframe/blob/main/notebooks/example.ipynb)
- [Issues](https://github.com/IvanildoBarauna/api-to-dataframe/issues)
