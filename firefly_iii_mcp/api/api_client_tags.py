from typing import Any

from .api_client_base import ApiClientBase


class ApiClientTags(ApiClientBase):
    """Firefly III `tags` domain API operations."""

    def list_attachment_by_tag(
        self, tag: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Lists all attachments."""
        return self.request("GET", f"/v1/tags/{tag}/attachments", params=params)

    def list_transaction_by_tag(
        self, tag: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all transactions with this tag."""
        return self.request("GET", f"/v1/tags/{tag}/transactions", params=params)

    def list_tag(self, params: dict | None = None) -> dict[str, Any]:
        """List all tags."""
        return self.request("GET", "/v1/tags", params=params)

    def store_tag(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new tag"""
        return self.request("POST", "/v1/tags", json=data, params=params)

    def get_tag(self, tag: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single tag."""
        return self.request("GET", f"/v1/tags/{tag}", params=params)

    def update_tag(
        self, tag: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing tag."""
        return self.request("PUT", f"/v1/tags/{tag}", json=data, params=params)

    def delete_tag(self, tag: str, params: dict | None = None) -> dict[str, Any]:
        """Delete an tag."""
        return self.request("DELETE", f"/v1/tags/{tag}", params=params)
