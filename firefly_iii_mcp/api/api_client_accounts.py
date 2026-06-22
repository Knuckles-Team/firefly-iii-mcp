from typing import Any

from .api_client_base import ApiClientBase


class ApiClientAccounts(ApiClientBase):
    """Firefly III `accounts` domain API operations."""

    def list_transaction_by_account(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions related to the account."""
        return self.request("GET", f"/v1/accounts/{id}/transactions", params=params)

    def list_attachment_by_account(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all attachments."""
        return self.request("GET", f"/v1/accounts/{id}/attachments", params=params)

    def list_piggy_bank_by_account(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all piggy banks related to the account."""
        return self.request("GET", f"/v1/accounts/{id}/piggy-banks", params=params)

    def list_account(self, params: dict | None = None) -> dict[str, Any]:
        """List all accounts."""
        return self.request("GET", "/v1/accounts", params=params)

    def store_account(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Create new account."""
        return self.request("POST", "/v1/accounts", json=data, params=params)

    def get_account(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get single account."""
        return self.request("GET", f"/v1/accounts/{id}", params=params)

    def update_account(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing account."""
        return self.request("PUT", f"/v1/accounts/{id}", json=data, params=params)

    def delete_account(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Permanently delete account."""
        return self.request("DELETE", f"/v1/accounts/{id}", params=params)
