from typing import Any

from .api_client_base import ApiClientBase


class ApiClientCharts(ApiClientBase):
    """Firefly III `charts` domain API operations."""

    def get_chart_account_overview(self, params: dict | None = None) -> dict[str, Any]:
        """Dashboard chart with asset account balance information."""
        return self.request("GET", "/v1/chart/account/overview", params=params)

    def get_chart_balance(self, params: dict | None = None) -> dict[str, Any]:
        """Dashboard chart with balance information."""
        return self.request("GET", "/v1/chart/balance/balance", params=params)

    def get_chart_budget_overview(self, params: dict | None = None) -> dict[str, Any]:
        """Dashboard chart with budget information."""
        return self.request("GET", "/v1/chart/budget/overview", params=params)

    def get_chart_category_overview(self, params: dict | None = None) -> dict[str, Any]:
        """Dashboard chart with category information."""
        return self.request("GET", "/v1/chart/category/overview", params=params)
