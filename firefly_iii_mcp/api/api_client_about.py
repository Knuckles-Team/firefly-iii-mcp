from typing import Any

from .api_client_base import ApiClientBase


class ApiClientAbout(ApiClientBase):
    """Firefly III `about` domain API operations."""

    def get_about(self, params: dict | None = None) -> dict[str, Any]:
        """System information end point."""
        return self.request("GET", "/v1/about", params=params)

    def get_current_user(self, params: dict | None = None) -> dict[str, Any]:
        """Currently authenticated user endpoint."""
        return self.request("GET", "/v1/about/user", params=params)

    def finish_batch(self, params: dict | None = None) -> dict[str, Any]:
        """Finish a batch of unprocessed transactions."""
        return self.request("POST", "/v1/batch/finish", params=params)

    def get_cron(self, cli_token: str, params: dict | None = None) -> dict[str, Any]:
        """Cron job endpoint"""
        return self.request("GET", f"/v1/cron/{cli_token}", params=params)
