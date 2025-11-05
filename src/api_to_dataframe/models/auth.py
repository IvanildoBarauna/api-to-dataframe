"""Authentication providers to enrich API requests with authorization headers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Callable, Dict, Optional, Tuple

AuthHeaders = Dict[str, str]
TokenWithExpiry = Tuple[str, Optional[datetime]]


class AuthProvider(ABC):
    """Represents a strategy capable of injecting authentication information."""

    @abstractmethod
    def apply(self, headers: Optional[AuthHeaders] = None) -> AuthHeaders:
        """Return request headers containing the required authentication details."""


class ApiKeyAuth(AuthProvider):
    """Static API key authentication added to a configurable header."""

    def __init__(self, header_name: str, api_key: str):
        """Store the header name and API key used for authenticated requests."""
        self.header_name = header_name
        self.api_key = api_key

    def apply(self, headers: Optional[AuthHeaders] = None) -> AuthHeaders:
        """Return headers with the API key injected into the configured header."""
        composed_headers = dict(headers or {})
        composed_headers[self.header_name] = self.api_key
        return composed_headers


class BearerTokenAuth(AuthProvider):
    """Bearer token authentication supporting automatic token refresh."""

    def __init__(
        self,
        token_supplier: Callable[[], TokenWithExpiry],
        *,
        header_name: str = "Authorization",
        scheme: str = "Bearer",
        refresh_margin: float = 0,
        clock: Callable[[], datetime] = datetime.utcnow,
    ):
        """Configure the bearer token strategy and how tokens are supplied."""
        self._token_supplier = token_supplier
        self.header_name = header_name
        self.scheme = scheme
        self._token: Optional[str] = None
        self._expires_at: Optional[datetime] = None
        self._refresh_margin = timedelta(seconds=refresh_margin)
        self._clock = clock

    def _ensure_token(self) -> None:
        """Fetch or refresh the bearer token when it is missing or expired."""
        if self._token is None or self._should_refresh():
            self._token, self._expires_at = self._token_supplier()

    def _should_refresh(self) -> bool:
        """Determine whether a new token is required based on the expiry time."""
        if self._expires_at is None:
            return False
        return self._expires_at <= self._clock() + self._refresh_margin

    def apply(self, headers: Optional[AuthHeaders] = None) -> AuthHeaders:
        """Return headers containing a valid bearer token with optional refresh."""
        self._ensure_token()
        composed_headers = dict(headers or {})
        composed_headers[self.header_name] = f"{self.scheme} {self._token}"
        return composed_headers


class OAuth2ClientCredentials(AuthProvider):
    """OAuth2 Client Credentials authentication with token renewal support."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        token_fetcher: Callable[[str, str, Optional[str]], TokenWithExpiry],
        *,
        scope: Optional[str] = None,
        header_name: str = "Authorization",
        refresh_margin: float = 30,
        clock: Callable[[], datetime] = datetime.utcnow,
    ):
        """Store client credentials and the callable responsible for new tokens."""
        self.client_id = client_id
        self.client_secret = client_secret
        self.scope = scope
        self._token_fetcher = token_fetcher
        self.header_name = header_name
        self._refresh_margin = timedelta(seconds=refresh_margin)
        self._clock = clock
        self._token: Optional[str] = None
        self._expires_at: Optional[datetime] = None

    def _ensure_token(self) -> None:
        """Obtain a valid OAuth2 access token using the configured fetcher."""
        if self._token is None or self._should_refresh():
            self._token, self._expires_at = self._token_fetcher(
                self.client_id, self.client_secret, self.scope
            )

    def _should_refresh(self) -> bool:
        """Determine whether the current OAuth2 token needs to be refreshed."""
        if self._expires_at is None:
            return False
        return self._expires_at <= self._clock() + self._refresh_margin

    def apply(self, headers: Optional[AuthHeaders] = None) -> AuthHeaders:
        """Return headers augmented with a fresh OAuth2 bearer token."""
        self._ensure_token()
        composed_headers = dict(headers or {})
        composed_headers[self.header_name] = f"Bearer {self._token}"
        return composed_headers

