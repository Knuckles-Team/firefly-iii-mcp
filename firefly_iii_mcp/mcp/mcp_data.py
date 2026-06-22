import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_data_tools(mcp: FastMCP):
    """Register `data` domain dynamic tools."""

    @mcp.tool(tags={"data"})
    async def data_operations(
        action: str = Field(
            description="Action to perform. One of: 'bulk_update_transactions', 'destroy_data', 'export_accounts', 'export_bills', 'export_budgets', 'export_categories', 'export_piggies', 'export_recurring', 'export_rules', 'export_tags', 'export_transactions', 'purge_data'."
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
        """Manage Firefly III `data` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing data tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "bulk_update_transactions",
                "destroy_data",
                "export_accounts",
                "export_bills",
                "export_budgets",
                "export_categories",
                "export_piggies",
                "export_recurring",
                "export_rules",
                "export_tags",
                "export_transactions",
                "purge_data",
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
