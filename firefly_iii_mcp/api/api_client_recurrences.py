from typing import Any

from .api_client_base import ApiClientBase


class ApiClientRecurrences(ApiClientBase):
    """Firefly III `recurrences` domain API operations."""

    def list_transaction_by_recurrence(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions created by a recurring transaction."""
        return self.request("GET", f"/v1/recurrences/{id}/transactions", params=params)

    def list_recurrence(self, params: dict | None = None) -> dict[str, Any]:
        """List all recurring transactions."""
        return self.request("GET", "/v1/recurrences", params=params)

    def store_recurrence(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new recurring transaction"""
        return self.request("POST", "/v1/recurrences", json=data, params=params)

    def get_recurrence(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single recurring transaction."""
        return self.request("GET", f"/v1/recurrences/{id}", params=params)

    def update_recurrence(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing recurring transaction."""
        return self.request("PUT", f"/v1/recurrences/{id}", json=data, params=params)

    def delete_recurrence(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a recurring transaction."""
        return self.request("DELETE", f"/v1/recurrences/{id}", params=params)

    def trigger_recurrence_recurrence(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Trigger the creation of a transaction for a specific recurring transaction"""
        return self.request("POST", f"/v1/recurrences/{id}/trigger", params=params)
