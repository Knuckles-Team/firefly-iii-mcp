from typing import Any

from .api_client_base import ApiClientBase


class ApiClientCurrencies(ApiClientBase):
    """Firefly III `currencies` domain API operations."""

    def list_account_by_currency(
        self, code: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all accounts with this currency."""
        return self.request("GET", f"/v1/currencies/{code}/accounts", params=params)

    def list_available_budget_by_currency(
        self, code: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all available budgets with this currency."""
        return self.request(
            "GET", f"/v1/currencies/{code}/available-budgets", params=params
        )

    def list_bill_by_currency(
        self, code: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all bills with this currency."""
        return self.request("GET", f"/v1/currencies/{code}/bills", params=params)

    def list_budget_limit_by_currency(
        self, code: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all budget limits with this currency"""
        return self.request(
            "GET", f"/v1/currencies/{code}/budget-limits", params=params
        )

    def list_recurrence_by_currency(
        self, code: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all recurring transactions with this currency."""
        return self.request("GET", f"/v1/currencies/{code}/recurrences", params=params)

    def list_rule_by_currency(
        self, code: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all rules with this currency."""
        return self.request("GET", f"/v1/currencies/{code}/rules", params=params)

    def list_transaction_by_currency(
        self, code: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions with this currency."""
        return self.request("GET", f"/v1/currencies/{code}/transactions", params=params)

    def list_currency(self, params: dict | None = None) -> dict[str, Any]:
        """List all currencies."""
        return self.request("GET", "/v1/currencies", params=params)

    def store_currency(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new currency"""
        return self.request("POST", "/v1/currencies", json=data, params=params)

    def enable_currency(self, code: str, params: dict | None = None) -> dict[str, Any]:
        """Enable a single currency."""
        return self.request("POST", f"/v1/currencies/{code}/enable", params=params)

    def disable_currency(self, code: str, params: dict | None = None) -> dict[str, Any]:
        """Disable a currency."""
        return self.request("POST", f"/v1/currencies/{code}/disable", params=params)

    def primary_currency(self, code: str, params: dict | None = None) -> dict[str, Any]:
        """Make currency primary currency."""
        return self.request("POST", f"/v1/currencies/{code}/primary", params=params)

    def get_currency(self, code: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single currency."""
        return self.request("GET", f"/v1/currencies/{code}", params=params)

    def update_currency(
        self, code: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing currency."""
        return self.request("PUT", f"/v1/currencies/{code}", json=data, params=params)

    def delete_currency(self, code: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a currency."""
        return self.request("DELETE", f"/v1/currencies/{code}", params=params)

    def get_primary_currency(self, params: dict | None = None) -> dict[str, Any]:
        """Get the primary currency of the current administration."""
        return self.request("GET", "/v1/currencies/primary", params=params)
