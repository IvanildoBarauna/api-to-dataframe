"""Unit tests for authentication providers."""
from datetime import datetime, timedelta

import pytest

from api_to_dataframe.models.auth import (
    ApiKeyAuth,
    BearerTokenAuth,
    OAuth2ClientCredentials,
)


class DummyClock:
    """Test helper that simulates the passage of time."""

    def __init__(self, start: datetime):
        """Initialize the dummy clock with the provided start time."""
        self._current = start

    def now(self) -> datetime:
        """Return the current mocked time."""
        return self._current

    def advance(self, seconds: float) -> None:
        """Advance the clock by the specified number of seconds."""
        self._current += timedelta(seconds=seconds)


class TokenSupplier:
    """Helper callable that returns sequential tokens for testing."""

    def __init__(self, tokens):
        """Store the list of tokens that will be returned sequentially."""
        self._tokens = list(tokens)
        self.calls = 0

    def __call__(self):
        """Return the next token with expiry information."""
        if not self._tokens:
            raise AssertionError("TokenSupplier invoked more times than expected")
        self.calls += 1
        return self._tokens.pop(0)


class OAuthFetcher:
    """Helper callable to emulate OAuth token retrieval with validation."""

    def __init__(self, expected_id: str, expected_secret: str, expected_scope: str, tokens):
        """Store expected credentials and queued tokens for assertions."""
        self.expected_id = expected_id
        self.expected_secret = expected_secret
        self.expected_scope = expected_scope
        self._tokens = list(tokens)
        self.calls = 0

    def __call__(self, client_id: str, client_secret: str, scope: str):
        """Return the next OAuth token ensuring credentials are forwarded."""
        assert client_id == self.expected_id
        assert client_secret == self.expected_secret
        assert scope == self.expected_scope
        if not self._tokens:
            raise AssertionError("OAuthFetcher invoked more times than expected")
        self.calls += 1
        return self._tokens.pop(0)


def test_api_key_auth_injects_header():
    """Ensure ApiKeyAuth injects a static header without mutating input."""
    provider = ApiKeyAuth("X-Api-Key", "secret")
    base_headers = {"Accept": "application/json"}

    result = provider.apply(base_headers)

    assert result["X-Api-Key"] == "secret"
    assert base_headers == {"Accept": "application/json"}


def test_bearer_token_auth_refreshes_when_expired():
    """Ensure BearerTokenAuth refreshes the token once the previous one expires."""
    start = datetime(2024, 1, 1, 0, 0, 0)
    clock = DummyClock(start)
    supplier = TokenSupplier(
        [
            ("token-one", start + timedelta(seconds=5)),
            ("token-two", start + timedelta(seconds=50)),
        ]
    )
    provider = BearerTokenAuth(
        supplier,
        refresh_margin=0,
        clock=clock.now,
    )

    headers_first = provider.apply({})
    clock.advance(10)
    headers_second = provider.apply({})

    assert headers_first["Authorization"] == "Bearer token-one"
    assert headers_second["Authorization"] == "Bearer token-two"
    assert supplier.calls == 2


def test_oauth_client_credentials_refreshes_token():
    """Ensure OAuth2ClientCredentials fetches a new token after expiration."""
    start = datetime(2024, 1, 1, 0, 0, 0)
    clock = DummyClock(start)
    fetcher = OAuthFetcher(
        "client-id",
        "client-secret",
        "scope.read",
        [
            ("oauth-token-one", start + timedelta(seconds=5)),
            ("oauth-token-two", start + timedelta(seconds=50)),
        ],
    )
    provider = OAuth2ClientCredentials(
        "client-id",
        "client-secret",
        fetcher,
        scope="scope.read",
        refresh_margin=0,
        clock=clock.now,
    )

    headers_first = provider.apply({})
    clock.advance(10)
    headers_second = provider.apply({})

    assert headers_first["Authorization"] == "Bearer oauth-token-one"
    assert headers_second["Authorization"] == "Bearer oauth-token-two"
    assert fetcher.calls == 2

    with pytest.raises(AssertionError):
        fetcher("client-id", "client-secret", "scope.read")
