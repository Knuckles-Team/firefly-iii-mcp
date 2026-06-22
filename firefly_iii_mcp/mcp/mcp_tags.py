import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_tags_tools(mcp: FastMCP):
    """Register `tags` domain dynamic tools."""

    @mcp.tool(tags={"tags"})
    async def tags_operations(
        action: str = Field(
            description="Action to perform. One of: 'delete_tag', 'get_tag', 'list_attachment_by_tag', 'list_tag', 'list_transaction_by_tag', 'store_tag', 'update_tag'."
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
        """Manage Firefly III `tags` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing tags tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {
                "delete_tag",
                "get_tag",
                "list_attachment_by_tag",
                "list_tag",
                "list_transaction_by_tag",
                "store_tag",
                "update_tag",
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
