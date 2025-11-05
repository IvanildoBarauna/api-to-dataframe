from copy import deepcopy
from typing import Any, Dict, Iterator, List, Optional, Union

from api_to_dataframe.models.retainer import retry_strategies, Strategies
from api_to_dataframe.models.get_data import GetData
from api_to_dataframe.models.pagination import (
    DataFetchResult,
    PaginationConfig,
    PaginationStrategy,
    PaginationStep,
    cursor_iterator,
    offset_limit_iterator,
    page_iterator,
)
from api_to_dataframe.utils.logger import logger


class ClientBuilder:
    def __init__(  # pylint: disable=too-many-positional-arguments,too-many-arguments
        self,
        endpoint: str,
        headers: dict = None,
        retry_strategy: Strategies = Strategies.NO_RETRY_STRATEGY,
        retries: int = 3,
        initial_delay: int = 1,
        connection_timeout: int = 1,
    ):
        """
        Initializes the ClientBuilder object.

        Args:
            endpoint (str): The API endpoint to connect to.
            headers (dict, optional): The headers to use for the API request. Defaults to None.
            retry_strategy (Strategies, optional): Defaults to Strategies.NO_RETRY_STRATEGY.
            retries (int): The number of times to retry a failed request. Defaults to 3.
            initial_delay (int): The delay between retries in seconds. Defaults to 1.
            connection_timeout (int): The timeout for the connection in seconds. Defaults to 1.

        Raises:
            ValueError: If endpoint is an empty string.
            ValueError: If retries is not a non-negative integer.
            ValueError: If delay is not a non-negative integer.
            ValueError: If connection_timeout is not a non-negative integer.
        """

        if headers is None:
            headers = {}
        if endpoint == "":
            error_msg = "endpoint cannot be an empty string"
            logger.error(error_msg)
            raise ValueError
        if not isinstance(retries, int) or retries < 0:
            error_msg = "retries must be a non-negative integer"
            logger.error(error_msg)
            raise ValueError
        if not isinstance(initial_delay, int) or initial_delay < 0:
            error_msg = "initial_delay must be a non-negative integer"
            logger.error(error_msg)
            raise ValueError
        if not isinstance(connection_timeout, int) or connection_timeout < 0:
            error_msg = "connection_timeout must be a non-negative integer"
            logger.error(error_msg)
            raise ValueError

        self.endpoint = endpoint
        self.retry_strategy = retry_strategy
        self.connection_timeout = connection_timeout
        self.headers = headers
        self.retries = retries
        self.delay = initial_delay
        self.pagination_config: Optional[PaginationConfig] = None

    def with_pagination(self, strategy: Union[PaginationStrategy, str], **strategy_kwargs) -> "ClientBuilder":
        """Configure pagination metadata to be used when fetching data."""

        if isinstance(strategy, PaginationStrategy):
            strategy_value = strategy
        elif isinstance(strategy, str):
            try:
                strategy_value = PaginationStrategy(strategy.lower())
            except ValueError as exc:
                error_msg = (
                    "Unsupported pagination strategy. Use one of: "
                    f"{', '.join(item.value for item in PaginationStrategy)}"
                )
                logger.error(error_msg)
                raise ValueError(error_msg) from exc
        else:
            error_msg = "Strategy must be a PaginationStrategy or string value"
            logger.error(error_msg)
            raise TypeError(error_msg)

        if strategy_value == PaginationStrategy.OFFSET_LIMIT:
            limit = strategy_kwargs.get("limit")
            if limit is None or not isinstance(limit, int) or limit <= 0:
                error_msg = "Offset/limit strategy requires a positive integer 'limit'"
                logger.error(error_msg)
                raise ValueError(error_msg)
        if strategy_value == PaginationStrategy.PAGE:
            start_page = strategy_kwargs.get("start_page", 1)
            if not isinstance(start_page, int) or start_page <= 0:
                error_msg = "Page strategy requires a positive integer 'start_page'"
                logger.error(error_msg)
                raise ValueError(error_msg)

        self.pagination_config = PaginationConfig(
            strategy=strategy_value,
            params=deepcopy(strategy_kwargs),
        )
        return self

    @retry_strategies
    def get_api_data(self):
        """
        Retrieves data from the API using the defined endpoint and retry strategy.

        This function sends a request to the API using the endpoint, headers, and
        connection timeout specified in the instance attributes. It uses the
        defined retry strategy to handle potential failures and retries.

        Returns:
            dict: The JSON response from the API as a dictionary.
        """
        if self.pagination_config is None:
            response = GetData.get_response(
                endpoint=self.endpoint,
                headers=self.headers,
                connection_timeout=self.connection_timeout,
            )
            payload = response.json()
            return DataFetchResult(
                payloads=[payload],
                records=_normalise_records(payload, results_key=None),
                metadata={"strategy": "single", "pages": 1},
            )

        iterator = self._build_iterator()
        payloads = []
        records = []
        metadata: Dict[str, Any] = {
            "strategy": self.pagination_config.strategy.value,
            "params": deepcopy(self.pagination_config.params),
            "pages": 0,
        }
        results_key = self.pagination_config.params.get("results_key")
        last_params: Optional[Dict[str, Any]] = None
        last_cursor: Optional[str] = None

        for step in iterator:
            payloads.append(step.payload)
            metadata["pages"] += 1
            last_params = step.params
            last_cursor = step.cursor

            step_records = _normalise_records(step.payload, results_key=results_key)
            records.extend(step_records)

        if last_params is not None:
            metadata["last_params"] = last_params
        if self.pagination_config.strategy == PaginationStrategy.CURSOR:
            metadata["last_cursor"] = last_cursor

        return DataFetchResult(payloads=payloads, records=records, metadata=metadata)

    @staticmethod
    def api_to_dataframe(response: Any):
        """
        Converts an API response to a DataFrame.

        This function takes a dictionary response from an API,
        uses the `to_dataframe` function from the `GetData` class
        to convert it into a DataFrame, and logs the operation as successful.

        Args:
            response (dict): The dictionary containing the API response.

        Returns:
            DataFrame: A pandas DataFrame containing the data from the API response.
        """
        if isinstance(response, DataFetchResult):
            records = response.as_records()
        else:
            records = response

        return GetData.to_dataframe(records)

    def _build_iterator(self) -> Iterator[PaginationStep]:
        """Create the configured pagination iterator."""

        assert self.pagination_config is not None  # for mypy style checking
        fetch_page = self._fetch_page
        params = self.pagination_config.params

        if self.pagination_config.strategy == PaginationStrategy.OFFSET_LIMIT:
            return offset_limit_iterator(fetch_page, **params)
        if self.pagination_config.strategy == PaginationStrategy.PAGE:
            return page_iterator(fetch_page, **params)
        if self.pagination_config.strategy == PaginationStrategy.CURSOR:
            return cursor_iterator(fetch_page, **params)

        error_msg = "Unsupported pagination strategy configured"
        logger.error(error_msg)
        raise ValueError(error_msg)

    def _fetch_page(self, params: Dict[str, Any]) -> Any:
        """Fetch a single page applying the current pagination parameters."""

        response = GetData.get_response(
            endpoint=self.endpoint,
            headers=self.headers,
            connection_timeout=self.connection_timeout,
            params=params if params else None,
        )
        return response.json()


def _normalise_records(payload: Any, results_key: Optional[str]) -> List[Any]:
    """Normalise payloads into a list of records."""

    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and results_key is not None:
        records = payload.get(results_key, [])
        return records if isinstance(records, list) else []
    return [payload]
