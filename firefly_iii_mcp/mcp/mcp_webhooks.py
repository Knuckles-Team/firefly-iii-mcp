import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_webhooks_tools(mcp: FastMCP):
    """Register `webhooks` domain dynamic tools."""

    @mcp.tool(tags={"webhooks"})
    async def webhooks_operations(
        action: str = Field(
            description="Action to perform. One of: 'delete_webhook', 'delete_webhook_message', 'delete_webhook_message_attempt', 'get_single_webhook_message', 'get_single_webhook_message_attempt', 'get_webhook', 'get_webhook_message_attempts', 'get_webhook_messages', 'list_webhook', 'store_webhook', 'submit_webhook', 'trigger_transaction_webhook', 'update_webhook'."
        ),
        params_json: str = Field(
            default="{}",
            description="JSON string of parameters (path params, 'data' body dict, and 'params' query dict) for the action.",
        ),
        client=Depends(get_client),
        ctx: Context | None = Field(
            default=None, description="MCP context for progress reporting"
        ),
    ) -> dict:
        """Manage Firefly III `webhooks` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing webhooks tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "delete_webhook",
                "delete_webhook_message",
                "delete_webhook_message_attempt",
                "get_single_webhook_message",
                "get_single_webhook_message_attempt",
                "get_webhook",
                "get_webhook_message_attempts",
                "get_webhook_messages",
                "list_webhook",
                "store_webhook",
                "submit_webhook",
                "trigger_transaction_webhook",
                "update_webhook",
            },
            service="firefly-iii",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved
        method = getattr(client, action, None)
        if method is None:
            return {"error": f"Unknown action: {action}"}
        return await run_blocking(method, **kwargs)
