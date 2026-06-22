from typing import Any

from .api_client_base import ApiClientBase


class ApiClientCategories(ApiClientBase):
    """Firefly III `categories` domain API operations."""

    def list_transaction_by_category(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions in a category."""
        return self.request("GET", f"/v1/categories/{id}/transactions", params=params)

    def list_attachment_by_category(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all attachments."""
        return self.request("GET", f"/v1/categories/{id}/attachments", params=params)

    def list_category(self, params: dict | None = None) -> dict[str, Any]:
        """List all categories."""
        return self.request("GET", "/v1/categories", params=params)

    def store_category(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new category"""
        return self.request("POST", "/v1/categories", json=data, params=params)

    def get_category(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single category."""
        return self.request("GET", f"/v1/categories/{id}", params=params)

    def update_category(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing category."""
        return self.request("PUT", f"/v1/categories/{id}", json=data, params=params)

    def delete_category(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a category."""
        return self.request("DELETE", f"/v1/categories/{id}", params=params)
