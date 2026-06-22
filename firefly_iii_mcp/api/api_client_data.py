from typing import Any

from .api_client_base import ApiClientBase


class ApiClientData(ApiClientBase):
    """Firefly III `data` domain API operations."""

    def bulk_update_transactions(self, params: dict | None = None) -> dict[str, Any]:
        """Bulk update transaction properties. For more information, see https://docs.firefly-iii.org/references/firefly-iii/api/specials/"""
        return self.request("POST", "/v1/data/bulk/transactions", params=params)

    def destroy_data(self, params: dict | None = None) -> dict[str, Any]:
        """Endpoint to destroy user data"""
        return self.request("DELETE", "/v1/data/destroy", params=params)

    def export_accounts(self, params: dict | None = None) -> dict[str, Any]:
        """Export account data from Firefly III"""
        return self.request("GET", "/v1/data/export/accounts", params=params)

    def export_bills(self, params: dict | None = None) -> dict[str, Any]:
        """Export bills from Firefly III"""
        return self.request("GET", "/v1/data/export/bills", params=params)

    def export_budgets(self, params: dict | None = None) -> dict[str, Any]:
        """Export budgets and budget amount data from Firefly III"""
        return self.request("GET", "/v1/data/export/budgets", params=params)

    def export_categories(self, params: dict | None = None) -> dict[str, Any]:
        """Export category data from Firefly III"""
        return self.request("GET", "/v1/data/export/categories", params=params)

    def export_piggies(self, params: dict | None = None) -> dict[str, Any]:
        """Export piggy banks from Firefly III"""
        return self.request("GET", "/v1/data/export/piggy-banks", params=params)

    def export_recurring(self, params: dict | None = None) -> dict[str, Any]:
        """Export recurring transaction data from Firefly III"""
        return self.request("GET", "/v1/data/export/recurring", params=params)

    def export_rules(self, params: dict | None = None) -> dict[str, Any]:
        """Export rule groups and rule data from Firefly III"""
        return self.request("GET", "/v1/data/export/rules", params=params)

    def export_tags(self, params: dict | None = None) -> dict[str, Any]:
        """Export tag data from Firefly III"""
        return self.request("GET", "/v1/data/export/tags", params=params)

    def export_transactions(self, params: dict | None = None) -> dict[str, Any]:
        """Export transaction data from Firefly III"""
        return self.request("GET", "/v1/data/export/transactions", params=params)

    def purge_data(self, params: dict | None = None) -> dict[str, Any]:
        """Endpoint to purge user data"""
        return self.request("DELETE", "/v1/data/purge", params=params)
