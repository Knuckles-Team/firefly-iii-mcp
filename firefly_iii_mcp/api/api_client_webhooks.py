from typing import Any

from .api_client_base import ApiClientBase


class ApiClientWebhooks(ApiClientBase):
    """Firefly III `webhooks` domain API operations."""

    def get_webhook_messages(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get all the messages of a single webhook."""
        return self.request("GET", f"/v1/webhooks/{id}/messages", params=params)

    def get_single_webhook_message(
        self, id: str, message_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get a single message from a webhook."""
        return self.request(
            "GET", f"/v1/webhooks/{id}/messages/{message_id}", params=params
        )

    def delete_webhook_message(
        self, id: str, message_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Delete a webhook message."""
        return self.request(
            "DELETE", f"/v1/webhooks/{id}/messages/{message_id}", params=params
        )

    def get_webhook_message_attempts(
        self, id: str, message_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get all the failed attempts of a single webhook message."""
        return self.request(
            "GET", f"/v1/webhooks/{id}/messages/{message_id}/attempts", params=params
        )

    def get_single_webhook_message_attempt(
        self, id: str, message_id: str, attempt_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Get a single failed attempt from a single webhook message."""
        return self.request(
            "GET",
            f"/v1/webhooks/{id}/messages/{message_id}/attempts/{attempt_id}",
            params=params,
        )

    def delete_webhook_message_attempt(
        self, id: str, message_id: str, attempt_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Delete a webhook attempt."""
        return self.request(
            "DELETE",
            f"/v1/webhooks/{id}/messages/{message_id}/attempts/{attempt_id}",
            params=params,
        )

    def submit_webhook(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Submit messages for a webhook."""
        return self.request("POST", f"/v1/webhooks/{id}/submit", params=params)

    def trigger_transaction_webhook(
        self, id: str, transaction_id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Trigger webhook for a given transaction."""
        return self.request(
            "POST",
            f"/v1/webhooks/{id}/trigger-transaction/{transaction_id}",
            params=params,
        )

    def list_webhook(self, params: dict | None = None) -> dict[str, Any]:
        """List all webhooks."""
        return self.request("GET", "/v1/webhooks", params=params)

    def store_webhook(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new webhook"""
        return self.request("POST", "/v1/webhooks", json=data, params=params)

    def get_webhook(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Get a single webhook."""
        return self.request("GET", f"/v1/webhooks/{id}", params=params)

    def update_webhook(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing webhook."""
        return self.request("PUT", f"/v1/webhooks/{id}", json=data, params=params)

    def delete_webhook(self, id: str, params: dict | None = None) -> dict[str, Any]:
        """Delete a webhook."""
        return self.request("DELETE", f"/v1/webhooks/{id}", params=params)
