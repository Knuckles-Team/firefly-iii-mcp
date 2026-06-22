import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_charts_tools(mcp: FastMCP):
    """Register `charts` domain dynamic tools."""

    @mcp.tool(tags={"charts"})
    async def charts_operations(
        action: str = Field(
            description="Action to perform. One of: 'get_chart_account_overview', 'get_chart_balance', 'get_chart_budget_overview', 'get_chart_category_overview'."
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
        """Manage Firefly III `charts` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing charts tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "get_chart_account_overview",
                "get_chart_balance",
                "get_chart_budget_overview",
                "get_chart_category_overview",
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
