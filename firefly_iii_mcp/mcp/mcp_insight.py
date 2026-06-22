import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_insight_tools(mcp: FastMCP):
    """Register `insight` domain dynamic tools."""

    @mcp.tool(tags={"insight"})
    async def insight_operations(
        action: str = Field(
            description="Action to perform. One of: 'insight_expense_asset', 'insight_expense_bill', 'insight_expense_budget', 'insight_expense_category', 'insight_expense_expense', 'insight_expense_no_bill', 'insight_expense_no_budget', 'insight_expense_no_category', 'insight_expense_no_tag', 'insight_expense_tag', 'insight_expense_total', 'insight_income_asset', 'insight_income_category', 'insight_income_no_category', 'insight_income_no_tag', 'insight_income_revenue', 'insight_income_tag', 'insight_income_total', 'insight_transfer_category', 'insight_transfer_no_category', 'insight_transfer_no_tag', 'insight_transfer_tag', 'insight_transfer_total', 'insight_transfers'."
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
        """Manage Firefly III `insight` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing insight tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "insight_expense_asset",
                "insight_expense_bill",
                "insight_expense_budget",
                "insight_expense_category",
                "insight_expense_expense",
                "insight_expense_no_bill",
                "insight_expense_no_budget",
                "insight_expense_no_category",
                "insight_expense_no_tag",
                "insight_expense_tag",
                "insight_expense_total",
                "insight_income_asset",
                "insight_income_category",
                "insight_income_no_category",
                "insight_income_no_tag",
                "insight_income_revenue",
                "insight_income_tag",
                "insight_income_total",
                "insight_transfer_category",
                "insight_transfer_no_category",
                "insight_transfer_no_tag",
                "insight_transfer_tag",
                "insight_transfer_total",
                "insight_transfers",
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
