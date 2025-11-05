from typing import Any, Optional, Sequence, Union

import pandas as pd
import requests

from api_to_dataframe.utils.logger import logger


class GetData:
    @staticmethod
    def get_response(endpoint: str, headers: dict, connection_timeout: int):
        # Make the request
        response = requests.get(endpoint, timeout=connection_timeout, headers=headers)

        # Attempt to raise for status to catch errors
        response.raise_for_status()

        return response

    @staticmethod
    def to_dataframe(
        response: Any,
        *,
        record_path: Optional[Union[str, Sequence[str]]] = None,
        meta: Optional[Sequence[Union[str, Sequence[str]]]] = None,
        errors: str = "raise",
        max_level: Optional[int] = None,
    ) -> pd.DataFrame:
        """Convert an API response object into a pandas DataFrame.

        Args:
            response (Any): The API response already decoded to a Python object.
            record_path (Optional[Union[str, Sequence[str]]]): The path to records for
                nested data structures accepted by :func:`pandas.json_normalize`.
            meta (Optional[Sequence[Union[str, Sequence[str]]]]): Additional metadata
                to include as columns in the resulting DataFrame.
            errors (str): Error handling strategy from
                :func:`pandas.json_normalize` ("raise" or "ignore").
            max_level (Optional[int]): Max depth to normalize nested records.

        Returns:
            pandas.DataFrame: A DataFrame containing the normalized data.

        Raises:
            ValueError: If the normalization results in an empty DataFrame while the
                error strategy is not set to ``"ignore"``.
        """

        if response is None or response == "":
            error_msg = "::: Response payload is empty :::"
            logger.error(error_msg)
            raise ValueError(error_msg)

        try:
            dataframe = pd.json_normalize(
                response,
                record_path=record_path,
                meta=meta,
                errors=errors,
                max_level=max_level,
            )
        except Exception as exc:  # pragma: no cover - defensive logging
            logger.error("::: Failed to normalize response: %s :::", exc)
            raise

        if dataframe.empty and errors != "ignore":
            error_msg = "::: DataFrame is empty :::"
            logger.error(error_msg)
            raise ValueError(error_msg)

        return dataframe
