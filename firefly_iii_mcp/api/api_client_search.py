from typing import Any

from .api_client_base import ApiClientBase


class ApiClientSearch(ApiClientBase):
    """Firefly III `search` domain API operations."""

    def search_accounts(self, params: dict | None = None) -> dict[str, Any]:
        """Search for accounts"""
        return self.request("GET", "/v1/search/accounts", params=params)

    def search_transactions(self, params: dict | None = None) -> dict[str, Any]:
        """Search for transactions"""
        return self.request("GET", "/v1/search/transactions", params=params)
