from typing import Any

from .api_client_base import ApiClientBase


class ApiClientRules(ApiClientBase):
    """Firefly III `rules` domain API operations."""

    def test_rule(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Test which transactions would be hit by the rule. No changes will be made."""
        return self.request("GET", f"/v1/rules/{id}/test", params=params)

    def fire_rule(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Fire the rule on your transactions."""
        return self.request("POST", f"/v1/rules/{id}/trigger", params=params)

    def list_rule(self, params: dict | None = None) -> dict[str, Any]:
        """List all rules."""
        return self.request("GET", "/v1/rules", params=params)

    def store_rule(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new rule"""
        return self.request("POST", "/v1/rules", json=data, params=params)

    def get_rule(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single rule."""
        return self.request("GET", f"/v1/rules/{id}", params=params)

    def update_rule(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing rule."""
        return self.request("PUT", f"/v1/rules/{id}", json=data, params=params)

    def delete_rule(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete an rule."""
        return self.request("DELETE", f"/v1/rules/{id}", params=params)
