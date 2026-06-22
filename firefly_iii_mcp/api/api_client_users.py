from typing import Any

from .api_client_base import ApiClientBase


class ApiClientUsers(ApiClientBase):
    """Firefly III `users` domain API operations."""

    def list_user(self, params: dict | None = None) -> dict[str, Any]:
        """List all users."""
        return self.request("GET", "/v1/users", params=params)

    def store_user(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new user"""
        return self.request("POST", "/v1/users", json=data, params=params)

    def get_user(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single user."""
        return self.request("GET", f"/v1/users/{id}", params=params)

    def update_user(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update an existing user's information."""
        return self.request("PUT", f"/v1/users/{id}", json=data, params=params)

    def delete_user(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a user."""
        return self.request("DELETE", f"/v1/users/{id}", params=params)
