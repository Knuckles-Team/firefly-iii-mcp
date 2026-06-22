import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_currency_exchange_rates_tools(mcp: FastMCP):
    """Register `currency_exchange_rates` domain dynamic tools."""

    @mcp.tool(tags={"currency-exchange-rates"})
    async def currency_exchange_rates_operations(
        action: str = Field(
            description="Action to perform. One of: 'delete_specific_currency_exchange_rate', 'delete_specific_currency_exchange_rate_on_date', 'delete_specific_currency_exchange_rates', 'list_currency_exchange_rates', 'list_specific_currency_exchange_rate', 'list_specific_currency_exchange_rate_on_date', 'list_specific_currency_exchange_rates', 'store_currency_exchange_rate', 'store_currency_exchange_rates_by_date', 'store_currency_exchange_rates_by_pair', 'update_currency_exchange_rate', 'update_currency_exchange_rate_by_date'."
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
        """Manage Firefly III `currency_exchange_rates` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing currency_exchange_rates tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "delete_specific_currency_exchange_rate",
                "delete_specific_currency_exchange_rate_on_date",
                "delete_specific_currency_exchange_rates",
                "list_currency_exchange_rates",
                "list_specific_currency_exchange_rate",
                "list_specific_currency_exchange_rate_on_date",
                "list_specific_currency_exchange_rates",
                "store_currency_exchange_rate",
                "store_currency_exchange_rates_by_date",
                "store_currency_exchange_rates_by_pair",
                "update_currency_exchange_rate",
                "update_currency_exchange_rate_by_date",
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
