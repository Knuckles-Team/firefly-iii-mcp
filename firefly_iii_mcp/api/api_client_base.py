from typing import Any
from urllib.parse import urlsplit

import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)


def _reject_unbounded_or_control_chars(
    value: str, max_length: int, error_message: str
) -> None:
    """Reject a value that is empty, oversized, or carries a header-injection
    control character (CR, LF, NUL)."""
    if not 1 <= len(value.encode("utf-8")) <= max_length or any(
        character in value for character in "\r\n\x00"
    ):
        raise ValueError(error_message)


def _validate_firefly_base_url(base_url: str) -> str:
    """Validate and normalize a Firefly III base URL.

    Rejects anything that is not an absolute, credential-free, query-free
    HTTPS URL of bounded length, then appends the API mount point if the
    caller did not already include it.
    """
    base_url = base_url.rstrip("/")
    _reject_unbounded_or_control_chars(base_url, 2_048, "Firefly III URL is invalid")
    parsed = urlsplit(base_url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError("Firefly III URL must be an absolute HTTPS URL")
    if parsed.username or parsed.password:
        raise ValueError("Firefly III URL must not contain credentials")
    if parsed.query or parsed.fragment:
        raise ValueError("Firefly III URL must not contain a query or fragment")
    # Firefly III mounts its REST API under /api; tolerate a base URL given
    # with or without the suffix.
    if not base_url.endswith("/api"):
        base_url = f"{base_url}/api"
    return base_url


def _validate_firefly_token(token: str) -> None:
    """Reject a bearer token that is out of bounds or could inject a header."""
    _reject_unbounded_or_control_chars(token, 65_536, "Firefly III token is invalid")


class ApiClientBase:
    """Base HTTP API client wrapper."""

    def __init__(
        self,
        base_url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        self.base_url = _validate_firefly_base_url(base_url)
        _validate_firefly_token(token)
        self.tls_profile = tls_profile or resolve_configured_tls_profile("firefly_iii")
        self.session = self.tls_profile.configure_requests_session(requests.Session())
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def close(self) -> None:
        """Release the HTTP session and process-lifetime TLS material."""
        self.session.close()
        self.tls_profile.cleanup()

    def request(self, method: str, path: str, **kwargs) -> dict[str, Any]:
        forbidden_transport_overrides = {"cert", "proxies", "verify"}.intersection(
            kwargs
        )
        if forbidden_transport_overrides:
            raise ValueError("per-request TLS policy overrides are not accepted")
        kwargs.setdefault("timeout", 30.0)
        kwargs.setdefault("allow_redirects", False)
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"status": response.status_code}
