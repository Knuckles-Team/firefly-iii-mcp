from typing import Any

from .api_client_base import ApiClientBase


class ApiClientLinks(ApiClientBase):
    """Firefly III `links` domain API operations."""

    def list_transaction_by_link_type(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions under this link type."""
        return self.request("GET", f"/v1/link-types/{id}/transactions", params=params)

    def list_link_type(self, params: dict | None = None) -> dict[str, Any]:
        """List all types of links."""
        return self.request("GET", "/v1/link-types", params=params)

    def store_link_type(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Create a new link type"""
        return self.request("POST", "/v1/link-types", json=data, params=params)

    def get_link_type(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get single a link type."""
        return self.request("GET", f"/v1/link-types/{id}", params=params)

    def update_link_type(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing link type."""
        return self.request("PUT", f"/v1/link-types/{id}", json=data, params=params)

    def delete_link_type(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Permanently delete link type."""
        return self.request("DELETE", f"/v1/link-types/{id}", params=params)

    def list_transaction_link(self, params: dict | None = None) -> dict[str, Any]:
        """List all transaction links."""
        return self.request("GET", "/v1/transaction-links", params=params)

    def store_transaction_link(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Create a new link between transactions"""
        return self.request("POST", "/v1/transaction-links", json=data, params=params)

    def get_transaction_link(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get a single link."""
        return self.request("GET", f"/v1/transaction-links/{id}", params=params)

    def delete_transaction_link(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Permanently delete link between transactions."""
        return self.request("DELETE", f"/v1/transaction-links/{id}", params=params)

    def update_transaction_link(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update an existing link between transactions."""
        return self.request(
            "PUT", f"/v1/transaction-links/{id}", json=data, params=params
        )
