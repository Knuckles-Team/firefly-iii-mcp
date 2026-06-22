from typing import Any

from .api_client_base import ApiClientBase


class ApiClientPreferences(ApiClientBase):
    """Firefly III `preferences` domain API operations."""

    def list_preference(self, params: dict | None = None) -> dict[str, Any]:
        """List all users preferences."""
        return self.request("GET", "/v1/preferences", params=params)

    def store_preference(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new preference for this user."""
        return self.request("POST", "/v1/preferences", json=data, params=params)

    def get_preference(self, name: str, params: dict | None = None) -> dict[str, Any]:
        """Return a single preference."""
        return self.request("GET", f"/v1/preferences/{name}", params=params)

    def update_preference(
        self, name: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update preference"""
        return self.request("PUT", f"/v1/preferences/{name}", json=data, params=params)
