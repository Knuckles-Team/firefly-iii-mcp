from typing import Any

from .api_client_base import ApiClientBase


class ApiClientConfiguration(ApiClientBase):
    """Firefly III `configuration` domain API operations."""

    def get_configuration(self, params: dict | None = None) -> dict[str, Any]:
        """Get Firefly III system configuration values."""
        return self.request("GET", "/v1/configuration", params=params)

    def get_single_configuration(
        self, name: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get a single Firefly III system configuration value"""
        return self.request("GET", f"/v1/configuration/{name}", params=params)

    def set_configuration(
        self, name: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update configuration value"""
        return self.request(
            "PUT", f"/v1/configuration/{name}", json=data, params=params
        )
