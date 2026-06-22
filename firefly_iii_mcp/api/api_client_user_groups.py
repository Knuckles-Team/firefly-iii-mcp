from typing import Any

from .api_client_base import ApiClientBase


class ApiClientUserGroups(ApiClientBase):
    """Firefly III `user_groups` domain API operations."""

    def list_user_groups(self, params: dict | None = None) -> dict[str, Any]:
        """List all the user groups available to this user."""
        return self.request("GET", "/v1/user-groups", params=params)

    def get_user_group(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single user group."""
        return self.request("GET", f"/v1/user-groups/{id}", params=params)

    def update_user_group(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update an existing user group."""
        return self.request("PUT", f"/v1/user-groups/{id}", json=data, params=params)
