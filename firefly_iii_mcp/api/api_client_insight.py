from typing import Any

from .api_client_base import ApiClientBase


class ApiClientInsight(ApiClientBase):
    """Firefly III `insight` domain API operations."""

    def insight_expense_expense(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, grouped by expense account."""
        return self.request("GET", "/v1/insight/expense/expense", params=params)

    def insight_expense_asset(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, grouped by asset account."""
        return self.request("GET", "/v1/insight/expense/asset", params=params)

    def insight_income_revenue(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into income, grouped by revenue account."""
        return self.request("GET", "/v1/insight/income/revenue", params=params)

    def insight_income_asset(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into income, grouped by asset account."""
        return self.request("GET", "/v1/insight/income/asset", params=params)

    def insight_transfers(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into transfers, grouped by account."""
        return self.request("GET", "/v1/insight/transfer/asset", params=params)

    def insight_expense_bill(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, grouped by bill."""
        return self.request("GET", "/v1/insight/expense/bill", params=params)

    def insight_expense_no_bill(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, without bill."""
        return self.request("GET", "/v1/insight/expense/no-bill", params=params)

    def insight_expense_budget(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, grouped by budget."""
        return self.request("GET", "/v1/insight/expense/budget", params=params)

    def insight_expense_no_budget(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, without budget."""
        return self.request("GET", "/v1/insight/expense/no-budget", params=params)

    def insight_expense_category(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, grouped by category."""
        return self.request("GET", "/v1/insight/expense/category", params=params)

    def insight_expense_no_category(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, without category."""
        return self.request("GET", "/v1/insight/expense/no-category", params=params)

    def insight_income_category(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into income, grouped by category."""
        return self.request("GET", "/v1/insight/income/category", params=params)

    def insight_income_no_category(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into income, without category."""
        return self.request("GET", "/v1/insight/income/no-category", params=params)

    def insight_transfer_category(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into transfers, grouped by category."""
        return self.request("GET", "/v1/insight/transfer/category", params=params)

    def insight_transfer_no_category(
        self, params: dict | None = None
    ) -> dict[str, Any]:
        """Insight into transfers, without category."""
        return self.request("GET", "/v1/insight/transfer/no-category", params=params)

    def insight_expense_tag(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, grouped by tag."""
        return self.request("GET", "/v1/insight/expense/tag", params=params)

    def insight_expense_no_tag(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, without tag."""
        return self.request("GET", "/v1/insight/expense/no-tag", params=params)

    def insight_income_tag(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into income, grouped by tag."""
        return self.request("GET", "/v1/insight/income/tag", params=params)

    def insight_income_no_tag(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into income, without tag."""
        return self.request("GET", "/v1/insight/income/no-tag", params=params)

    def insight_transfer_tag(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into transfers, grouped by tag."""
        return self.request("GET", "/v1/insight/transfer/tag", params=params)

    def insight_transfer_no_tag(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into expenses, without tag."""
        return self.request("GET", "/v1/insight/transfer/no-tag", params=params)

    def insight_expense_total(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into total expenses."""
        return self.request("GET", "/v1/insight/expense/total", params=params)

    def insight_income_total(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into total income."""
        return self.request("GET", "/v1/insight/income/total", params=params)

    def insight_transfer_total(self, params: dict | None = None) -> dict[str, Any]:
        """Insight into total transfers."""
        return self.request("GET", "/v1/insight/transfer/total", params=params)
