from typing import Any

from .api_client_base import ApiClientBase


class ApiClientTransactions(ApiClientBase):
    """Firefly III `transactions` domain API operations."""

    def list_links_by_journal(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all the transaction links for an individual journal (individual split)."""
        return self.request(
            "GET", f"/v1/transaction-journals/{id}/links", params=params
        )

    def get_transaction_by_journal(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get a single transaction, based on one of the underlying transaction journals (transaction splits)."""
        return self.request("GET", f"/v1/transaction-journals/{id}", params=params)

    def delete_transaction_journal(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Delete split from transaction"""
        return self.request("DELETE", f"/v1/transaction-journals/{id}", params=params)

    def list_attachment_by_transaction(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all attachments."""
        return self.request("GET", f"/v1/transactions/{id}/attachments", params=params)

    def list_event_by_transaction(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all piggy bank events."""
        return self.request(
            "GET", f"/v1/transactions/{id}/piggy-bank-events", params=params
        )

    def list_transaction(self, params: dict | None = None) -> dict[str, Any]:
        """List all the user's transactions."""
        return self.request("GET", "/v1/transactions", params=params)

    def store_transaction(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new transaction"""
        return self.request("POST", "/v1/transactions", json=data, params=params)

    def get_transaction(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single transaction."""
        return self.request("GET", f"/v1/transactions/{id}", params=params)

    def update_transaction(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing transaction. For more information, see https://docs.firefly-iii.org/references/firefly-iii/api/specials/"""
        return self.request("PUT", f"/v1/transactions/{id}", json=data, params=params)

    def delete_transaction(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a transaction."""
        return self.request("DELETE", f"/v1/transactions/{id}", params=params)
