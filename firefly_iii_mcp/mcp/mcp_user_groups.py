import json

from agent_utilities.mcp_utilities import resolve_action, run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def register_user_groups_tools(mcp: FastMCP):
    """Register `user_groups` domain dynamic tools."""

    @mcp.tool(tags={"user-groups"})
    async def user_groups_operations(
        action: str = Field(
            description="Action to perform. One of: 'get_user_group', 'list_user_groups', 'update_user_group'."
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
        """Manage Firefly III `user_groups` operations. CONCEPT:FF-001"""
        if ctx:
            await ctx.info("Executing user_groups tool...")
        try:
            kwargs = json.loads(params_json)
        except Exception as e:
            return {"error": f"Invalid params_json: {e}"}
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        resolved = resolve_action(
            action,
            {"get_user_group", "list_user_groups", "update_user_group"},
            service="firefly-iii",
        )
        if isinstance(resolved, dict):
            return resolved
        action = resolved
        method = getattr(client, action, None)
        if method is None:
            return {"error": f"Unknown action: {action}"}
        return await run_blocking(method, **kwargs)
