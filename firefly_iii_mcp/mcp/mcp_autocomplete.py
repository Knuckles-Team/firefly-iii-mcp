import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_autocomplete_tools(mcp: FastMCP):
    """Register `autocomplete` domain dynamic tools."""

    @mcp.tool(tags={"autocomplete"})
    async def autocomplete_operations(
        action: str = Field(
            description="Action to perform. One of: 'get_accounts_ac', 'get_bills_ac', 'get_budgets_ac', 'get_categories_ac', 'get_currencies_ac', 'get_currencies_code_ac', 'get_object_groups_ac', 'get_piggies_ac', 'get_piggies_balance_ac', 'get_recurring_ac', 'get_rule_groups_ac', 'get_rules_ac', 'get_subscriptions_ac', 'get_tag_ac', 'get_transaction_types_ac', 'get_transactions_ac', 'get_transactions_idac'."
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
        """Manage Firefly III `autocomplete` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing autocomplete tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "get_accounts_ac",
                "get_bills_ac",
                "get_budgets_ac",
                "get_categories_ac",
                "get_currencies_ac",
                "get_currencies_code_ac",
                "get_object_groups_ac",
                "get_piggies_ac",
                "get_piggies_balance_ac",
                "get_recurring_ac",
                "get_rule_groups_ac",
                "get_rules_ac",
                "get_subscriptions_ac",
                "get_tag_ac",
                "get_transaction_types_ac",
                "get_transactions_ac",
                "get_transactions_idac",
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
