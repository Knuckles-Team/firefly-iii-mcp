from typing import Any

from .api_client_base import ApiClientBase


class ApiClientAttachments(ApiClientBase):
    """Firefly III `attachments` domain API operations."""

    def list_attachment(self, params: dict | None = None) -> dict[str, Any]:
        """List all attachments."""
        return self.request("GET", "/v1/attachments", params=params)

    def store_attachment(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new attachment."""
        return self.request("POST", "/v1/attachments", json=data, params=params)

    def get_attachment(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single attachment."""
        return self.request("GET", f"/v1/attachments/{id}", params=params)

    def update_attachment(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing attachment."""
        return self.request("PUT", f"/v1/attachments/{id}", json=data, params=params)

    def delete_attachment(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete an attachment."""
        return self.request("DELETE", f"/v1/attachments/{id}", params=params)

    def download_attachment(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Download a single attachment."""
        return self.request("GET", f"/v1/attachments/{id}/download", params=params)

    def upload_attachment(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Upload an attachment."""
        return self.request(
            "POST", f"/v1/attachments/{id}/upload", json=data, params=params
        )
