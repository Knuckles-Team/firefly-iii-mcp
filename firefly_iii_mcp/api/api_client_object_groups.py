from typing import Any

from .api_client_base import ApiClientBase


class ApiClientObjectGroups(ApiClientBase):
    """Firefly III `object_groups` domain API operations."""

    def list_piggy_bank_by_object_group(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all piggy banks related to the object group."""
        return self.request("GET", f"/v1/object-groups/{id}/piggy-banks", params=params)

    def list_bill_by_object_group(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all bills with this object group."""
        return self.request("GET", f"/v1/object-groups/{id}/bills", params=params)

    def list_object_groups(self, params: dict | None = None) -> dict[str, Any]:
        """List all object groups."""
        return self.request("GET", "/v1/object-groups", params=params)

    def get_object_group(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single object group."""
        return self.request("GET", f"/v1/object-groups/{id}", params=params)

    def update_object_group(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing object group."""
        return self.request("PUT", f"/v1/object-groups/{id}", json=data, params=params)

    def delete_object_group(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Delete a object group."""
        return self.request("DELETE", f"/v1/object-groups/{id}", params=params)
