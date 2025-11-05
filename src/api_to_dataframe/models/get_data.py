from typing import Any, Dict, Optional

import pandas as pd
import requests

from api_to_dataframe.utils.logger import logger


class GetData:
    @staticmethod
    def get_response(  # pylint: disable=too-many-arguments,too-many-positional-arguments
        endpoint: str,
        headers: Optional[Dict[str, str]],
        connection_timeout: int,
        method: str = "GET",
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Any] = None,
        data: Optional[Any] = None,
        files: Optional[Any] = None,
        auth: Optional[Any] = None,
        session: Optional[requests.Session] = None,
    ):
        """Execute an HTTP request and return the raw response."""

        if not isinstance(method, str) or not method.strip():
            error_msg = "method must be a non-empty string"
            logger.error(error_msg)
            raise ValueError(error_msg)

        request_callable = session.request if session else requests.request

        response = request_callable(
            method=method.upper(),
            url=endpoint,
            timeout=connection_timeout,
            headers=headers,
            params=params,
            json=json,
            data=data,
            files=files,
            auth=auth,
        )

        response.raise_for_status()

        return response

    @staticmethod
    def to_dataframe(response):
        """Convert an API response payload into a pandas DataFrame."""
        df = pd.DataFrame(response)

        # Check if DataFrame is empty
        if df.empty:
            error_msg = "::: DataFrame is empty :::"
            logger.error(error_msg)
            raise ValueError(error_msg)

        return df
