import json
from typing import Literal

from agent_connector_sdk.mcp.action_dispatch import resolve_action
from agent_connector_sdk.mcp.concurrency import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_accounts_tools(mcp: FastMCP):
    """Register `accounts` domain dynamic tools."""

    @mcp.tool(
        tags={"accounts"},
        annotations={
            "readOnlyHint": False,
            "destructiveHint": True,
            "idempotentHint": False,
            "openWorldHint": True,
        },
        meta={
            "eg.annotations": {"modalities_in": ["text"], "modalities_out": ["text"]}
        },
    )
    async def accounts_operations(
        action: Literal[
            "delete_account",
            "get_account",
            "list_account",
            "list_attachment_by_account",
            "list_piggy_bank_by_account",
            "list_transaction_by_account",
            "store_account",
            "update_account",
        ] = Field(
            description="Action to perform. One of: 'delete_account', 'get_account', 'list_account', 'list_attachment_by_account', 'list_piggy_bank_by_account', 'list_transaction_by_account', 'store_account', 'update_account'."
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
        """Manage Firefly III `accounts` operations. CONCEPT:FF-OS.config.ff"""
        if ctx:
            await ctx.info("Executing accounts tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "delete_account",
                "get_account",
                "list_account",
                "list_attachment_by_account",
                "list_piggy_bank_by_account",
                "list_transaction_by_account",
                "store_account",
                "update_account",
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
