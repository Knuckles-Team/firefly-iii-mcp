from typing import Any

from .api_client_base import ApiClientBase


class ApiClientPiggyBanks(ApiClientBase):
    """Firefly III `piggy_banks` domain API operations."""

    def list_event_by_piggy_bank(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all events linked to a piggy bank."""
        return self.request("GET", f"/v1/piggy-banks/{id}/events", params=params)

    def list_attachment_by_piggy_bank(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all attachments."""
        return self.request("GET", f"/v1/piggy-banks/{id}/attachments", params=params)

    def list_piggy_bank(self, params: dict | None = None) -> dict[str, Any]:
        """List all piggy banks."""
        return self.request("GET", "/v1/piggy-banks", params=params)

    def store_piggy_bank(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new piggy bank"""
        return self.request("POST", "/v1/piggy-banks", json=data, params=params)

    def get_piggy_bank(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single piggy bank."""
        return self.request("GET", f"/v1/piggy-banks/{id}", params=params)

    def update_piggy_bank(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing piggy bank."""
        return self.request("PUT", f"/v1/piggy-banks/{id}", json=data, params=params)

    def delete_piggy_bank(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a piggy bank."""
        return self.request("DELETE", f"/v1/piggy-banks/{id}", params=params)
