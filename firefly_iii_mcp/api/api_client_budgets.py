from typing import Any

from .api_client_base import ApiClientBase


class ApiClientBudgets(ApiClientBase):
    """Firefly III `budgets` domain API operations."""

    def list_transaction_by_budget_limit(
        self, id: str, limit_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions by a budget limit ID."""
        return self.request(
            "GET", f"/v1/budgets/{id}/limits/{limit_id}/transactions", params=params
        )

    def list_budget_limit_by_budget(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get all limits for a budget."""
        return self.request("GET", f"/v1/budgets/{id}/limits", params=params)

    def store_budget_limit(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store new budget limit."""
        return self.request(
            "POST", f"/v1/budgets/{id}/limits", json=data, params=params
        )

    def get_budget_limit(
        self, id: str, limit_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get single budget limit."""
        return self.request("GET", f"/v1/budgets/{id}/limits/{limit_id}", params=params)

    def update_budget_limit(
        self,
        id: str,
        limit_id: str,
        data: dict | None = None,
        params: dict | None = None,
    ) -> dict[str, Any]:
        """Update existing budget limit."""
        return self.request(
            "PUT", f"/v1/budgets/{id}/limits/{limit_id}", json=data, params=params
        )

    def delete_budget_limit(
        self, id: str, limit_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Delete a budget limit."""
        return self.request(
            "DELETE", f"/v1/budgets/{id}/limits/{limit_id}", params=params
        )

    def list_budget_limit(self, params: dict | None = None) -> dict[str, Any]:
        """Get list of budget limits by date"""
        return self.request("GET", "/v1/budget-limits", params=params)

    def list_transaction_by_budget(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """All transactions to a budget."""
        return self.request("GET", f"/v1/budgets/{id}/transactions", params=params)

    def list_attachment_by_budget(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all attachments of a budget."""
        return self.request("GET", f"/v1/budgets/{id}/attachments", params=params)

    def list_transaction_without_budget(
        self, params: dict | None = None
    ) -> dict[str, Any]:
        """All transactions without a budget."""
        return self.request(
            "GET", "/v1/budgets/transactions-without-budget", params=params
        )

    def list_budget(self, params: dict | None = None) -> dict[str, Any]:
        """List all budgets."""
        return self.request("GET", "/v1/budgets", params=params)

    def store_budget(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new budget"""
        return self.request("POST", "/v1/budgets", json=data, params=params)

    def get_budget(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single budget."""
        return self.request("GET", f"/v1/budgets/{id}", params=params)

    def update_budget(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing budget."""
        return self.request("PUT", f"/v1/budgets/{id}", json=data, params=params)

    def delete_budget(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a budget."""
        return self.request("DELETE", f"/v1/budgets/{id}", params=params)
