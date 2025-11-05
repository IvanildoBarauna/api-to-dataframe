"""Pagination helpers and data structures."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Dict, Iterator, List, Optional


class PaginationStrategy(str, Enum):
    """Describe the supported pagination strategies."""

    OFFSET_LIMIT = "offset_limit"
    PAGE = "page"
    CURSOR = "cursor"


@dataclass
class PaginationConfig:
    """Store pagination strategy metadata for the client."""

    strategy: PaginationStrategy
    params: Dict[str, Any]


@dataclass
class PaginationStep:
    """Hold a single pagination iteration payload and context."""

    payload: Any
    params: Dict[str, Any]
    cursor: Optional[str] = None


@dataclass
class DataFetchResult:
    """Represent the aggregated result of a paginated fetch."""

    payloads: List[Any]
    records: List[Any]
    metadata: Dict[str, Any]

    def as_records(self) -> List[Any]:
        """Return the aggregated list of records."""

        return self.records


def offset_limit_iterator(
    fetch_page: Callable[[Dict[str, Any]], Any],
    *,
    limit: int,
    offset: int = 0,
    offset_param: str = "offset",
    limit_param: str = "limit",
    max_pages: Optional[int] = None,
    results_key: Optional[str] = None,
    stop_on_short_page: bool = True,
) -> Iterator[PaginationStep]:
    """Iterate over pages using an ``offset``/``limit`` pattern."""

    current_offset = offset
    page_number = 0

    while True:
        params = {offset_param: current_offset, limit_param: limit}
        page = fetch_page(params)
        yield PaginationStep(payload=page, params=params)
        page_number += 1

        if _should_stop(page, results_key=results_key, expected_length=limit, stop_on_short_page=stop_on_short_page):
            break

        current_offset += limit
        if max_pages is not None and page_number >= max_pages:
            break


def page_iterator(
    fetch_page: Callable[[Dict[str, Any]], Any],
    *,
    start_page: int = 1,
    page_param: str = "page",
    max_pages: Optional[int] = None,
    results_key: Optional[str] = None,
    stop_on_empty: bool = True,
) -> Iterator[PaginationStep]:
    """Iterate over pages using numeric page indexes."""

    current_page = start_page
    page_number = 0

    while True:
        params = {page_param: current_page}
        page = fetch_page(params)
        yield PaginationStep(payload=page, params=params)
        page_number += 1

        if _should_stop(page, results_key=results_key, stop_on_empty=stop_on_empty):
            break

        current_page += 1
        if max_pages is not None and page_number >= max_pages:
            break


def cursor_iterator(
    fetch_page: Callable[[Dict[str, Any]], Any],
    *,
    cursor_param: str = "cursor",
    initial_cursor: Optional[str] = None,
    next_cursor_key: str = "next_cursor",
    max_pages: Optional[int] = None,
    results_key: Optional[str] = None,
    stop_on_empty: bool = True,
) -> Iterator[PaginationStep]:
    """Iterate using cursor-based pagination."""

    cursor = initial_cursor
    page_number = 0

    while True:
        params: Dict[str, Any] = {}
        if cursor is not None:
            params[cursor_param] = cursor

        page = fetch_page(params)
        next_cursor = _extract_next_cursor(page, next_cursor_key)
        yield PaginationStep(payload=page, params=params, cursor=next_cursor)
        page_number += 1

        if _should_stop(page, results_key=results_key, stop_on_empty=stop_on_empty):
            break

        if max_pages is not None and page_number >= max_pages:
            break

        if next_cursor is None:
            break

        cursor = next_cursor


def _should_stop(
    page: Any,
    *,
    results_key: Optional[str],
    expected_length: Optional[int] = None,
    stop_on_short_page: bool = False,
    stop_on_empty: bool = False,
) -> bool:
    """Evaluate whether pagination should stop based on the payload."""

    if page is None:
        return True

    items = _extract_items(page, results_key)
    if items is None:
        return False

    if stop_on_empty and len(items) == 0:
        return True

    if expected_length is not None and stop_on_short_page and len(items) < expected_length:
        return True

    return False


def _extract_items(page: Any, results_key: Optional[str]) -> Optional[List[Any]]:
    """Extract a list of items from the payload when possible."""

    if isinstance(page, list):
        return page

    if isinstance(page, dict):
        if results_key is None:
            return None
        items = page.get(results_key, [])
        return items if isinstance(items, list) else []

    return None


def _extract_next_cursor(page: Any, next_cursor_key: str) -> Optional[str]:
    """Extract the cursor value from a response payload."""

    if isinstance(page, dict):
        cursor = page.get(next_cursor_key)
        if isinstance(cursor, str) or cursor is None:
            return cursor
    return None
