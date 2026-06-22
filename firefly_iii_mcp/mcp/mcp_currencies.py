import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_currencies_tools(mcp: FastMCP):
    """Register `currencies` domain dynamic tools."""

    @mcp.tool(tags={"currencies"})
    async def currencies_operations(
        action: str = Field(
            description="Action to perform. One of: 'delete_currency', 'disable_currency', 'enable_currency', 'get_currency', 'get_primary_currency', 'list_account_by_currency', 'list_available_budget_by_currency', 'list_bill_by_currency', 'list_budget_limit_by_currency', 'list_currency', 'list_recurrence_by_currency', 'list_rule_by_currency', 'list_transaction_by_currency', 'primary_currency', 'store_currency', 'update_currency'."
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
        """Manage Firefly III `currencies` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing currencies tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "delete_currency",
                "disable_currency",
                "enable_currency",
                "get_currency",
                "get_primary_currency",
                "list_account_by_currency",
                "list_available_budget_by_currency",
                "list_bill_by_currency",
                "list_budget_limit_by_currency",
                "list_currency",
                "list_recurrence_by_currency",
                "list_rule_by_currency",
                "list_transaction_by_currency",
                "primary_currency",
                "store_currency",
                "update_currency",
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
