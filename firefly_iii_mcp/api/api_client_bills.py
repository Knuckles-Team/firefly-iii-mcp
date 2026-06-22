from typing import Any

from .api_client_base import ApiClientBase


class ApiClientBills(ApiClientBase):
    """Firefly III `bills` domain API operations."""

    def list_attachment_by_bill(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all attachments uploaded to the bill."""
        return self.request("GET", f"/v1/bills/{id}/attachments", params=params)

    def list_rule_by_bill(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """List all rules associated with the bill."""
        return self.request("GET", f"/v1/bills/{id}/rules", params=params)

    def list_transaction_by_bill(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions associated with the  bill."""
        return self.request("GET", f"/v1/bills/{id}/transactions", params=params)

    def list_bill(self, params: dict | None = None) -> dict[str, Any]:
        """List all bills."""
        return self.request("GET", "/v1/bills", params=params)

    def store_bill(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new bill"""
        return self.request("POST", "/v1/bills", json=data, params=params)

    def get_bill(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single bill."""
        return self.request("GET", f"/v1/bills/{id}", params=params)

    def update_bill(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing bill."""
        return self.request("PUT", f"/v1/bills/{id}", json=data, params=params)

    def delete_bill(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a bill."""
        return self.request("DELETE", f"/v1/bills/{id}", params=params)
