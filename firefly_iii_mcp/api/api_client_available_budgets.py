from typing import Any

from .api_client_base import ApiClientBase


class ApiClientAvailableBudgets(ApiClientBase):
    """Firefly III `available_budgets` domain API operations."""

    def list_available_budgets(self, params: dict | None = None) -> dict[str, Any]:
        """List all available budget amounts."""
        return self.request("GET", "/v1/available-budgets", params=params)

    def get_available_budget(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get a single available budget."""
        return self.request("GET", f"/v1/available-budgets/{id}", params=params)
