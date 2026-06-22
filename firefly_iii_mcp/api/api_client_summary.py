from typing import Any

from .api_client_base import ApiClientBase


class ApiClientSummary(ApiClientBase):
    """Firefly III `summary` domain API operations."""

    def get_basic_summary(self, params: dict | None = None) -> dict[str, Any]:
        """Returns basic sums of the users data."""
        return self.request("GET", "/v1/summary/basic", params=params)
