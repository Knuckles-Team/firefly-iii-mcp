from typing import Any

from .api_client_base import ApiClientBase


class ApiClientRuleGroups(ApiClientBase):
    """Firefly III `rule_groups` domain API operations."""

    def list_rule_by_group(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """List rules in this rule group."""
        return self.request("GET", f"/v1/rule-groups/{id}/rules", params=params)

    def test_rule_group(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Test which transactions would be hit by the rule group. No changes will be made."""
        return self.request("GET", f"/v1/rule-groups/{id}/test", params=params)

    def fire_rule_group(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Fire the rule group on your transactions."""
        return self.request("POST", f"/v1/rule-groups/{id}/trigger", params=params)

    def list_rule_group(self, params: dict | None = None) -> dict[str, Any]:
        """List all rule groups."""
        return self.request("GET", "/v1/rule-groups", params=params)

    def store_rule_group(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new rule group."""
        return self.request("POST", "/v1/rule-groups", json=data, params=params)

    def get_rule_group(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single rule group."""
        return self.request("GET", f"/v1/rule-groups/{id}", params=params)

    def update_rule_group(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing rule group."""
        return self.request("PUT", f"/v1/rule-groups/{id}", json=data, params=params)

    def delete_rule_group(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a rule group."""
        return self.request("DELETE", f"/v1/rule-groups/{id}", params=params)
