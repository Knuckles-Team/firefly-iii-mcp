from typing import Any
from urllib.parse import urlsplit

import requests
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)


class ApiClientBase:
    """Base HTTP API client wrapper."""

    def __init__(
        self,
        base_url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
    ):
        base_url = base_url.rstrip("/")
        if not 1 <= len(base_url.encode("utf-8")) <= 2_048 or any(
            character in base_url for character in "\r\n\x00"
        ):
            raise ValueError("Firefly III URL is invalid")
        parsed = urlsplit(base_url)
        if parsed.scheme != "https" or not parsed.hostname:
            raise ValueError("Firefly III URL must be an absolute HTTPS URL")
        if parsed.username or parsed.password:
            raise ValueError("Firefly III URL must not contain credentials")
        if parsed.query or parsed.fragment:
            raise ValueError("Firefly III URL must not contain a query or fragment")
        if not 1 <= len(token.encode("utf-8")) <= 65_536 or any(
            character in token for character in "\r\n\x00"
        ):
            raise ValueError("Firefly III token is invalid")
        # Firefly III mounts its REST API under /api; tolerate a base URL given
        # with or without the suffix.
        if not base_url.endswith("/api"):
            base_url = f"{base_url}/api"
        self.base_url = base_url
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
