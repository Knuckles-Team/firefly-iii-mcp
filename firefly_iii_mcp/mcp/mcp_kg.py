"""Native knowledge-graph ingestion tools for Firefly III (Wire-First surface).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. Registers ``firefly_ingest_*``
tools that list the real Firefly III records via the API client and push them into
the epistemic-graph knowledge graph as typed OWL nodes (``:Account`` / ``:Transaction``
/ ``:Budget`` + links). Auto-discovered by ``register_tool_surface`` (tag ``kg``,
gated by ``setting("KGTOOL", True)``); best-effort — returns ``{"ingested": None}``
when no engine is reachable.
"""

import json

from agent_utilities.mcp_utilities import run_blocking
from fastmcp import Context, FastMCP
from fastmcp.dependencies import Depends
from pydantic import Field

from ..auth import get_client


def _records(resp) -> list[dict]:
    """Normalize a Firefly JSON:API response into a list of resource dicts."""
    data = getattr(resp, "data", resp)
    if isinstance(data, dict):
        data = data.get("data", data)
    if isinstance(data, list):
        return [r for r in data if r is not None]
    return [data] if data is not None else []


def register_kg_tools(mcp: FastMCP):
    """Register `kg` domain native-ingestion tools."""

    @mcp.tool(tags={"kg"})
    async def firefly_ingest_accounts(
        params_json: str = Field(
            default="{}",
            description='JSON string of list_account query params (e.g. {"params": {"type": "asset"}}).',
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Natively ingest Firefly III accounts into epistemic-graph as typed :Account nodes.

        Lists accounts via the API and pushes them (with their :Currency + :denominatedIn
        links) into the knowledge graph via the fast engine client. CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from ..kg_ingest import ingest_accounts

        if ctx:
            await ctx.info("Ingesting Firefly III accounts...")
        kwargs = json.loads(params_json) if params_json else {}
        resp = await run_blocking(client.list_account, **kwargs)
        records = _records(resp)
        return {"listed": len(records), "ingested": ingest_accounts(records)}

    @mcp.tool(tags={"kg"})
    async def firefly_ingest_transactions(
        params_json: str = Field(
            default="{}",
            description='JSON string of list_transaction query params (e.g. {"params": {"start": "2026-01-01", "end": "2026-12-31"}}).',
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Natively ingest Firefly III transactions into epistemic-graph as typed :Transaction nodes.

        Lists transactions via the API and pushes them (with :sourceAccount /
        :destinationAccount / :inBudget / :inCategory links) into the knowledge graph.
        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from ..kg_ingest import ingest_transactions

        if ctx:
            await ctx.info("Ingesting Firefly III transactions...")
        kwargs = json.loads(params_json) if params_json else {}
        resp = await run_blocking(client.list_transaction, **kwargs)
        records = _records(resp)
        return {"listed": len(records), "ingested": ingest_transactions(records)}

    @mcp.tool(tags={"kg"})
    async def firefly_ingest_budgets(
        params_json: str = Field(
            default="{}",
            description="JSON string of list_budget query params.",
        ),
        client=Depends(get_client),
        ctx: Context | None = None,
    ) -> dict:
        """Natively ingest Firefly III budgets into epistemic-graph as typed :Budget nodes.

        CONCEPT:AU-KG.ingest.enterprise-source-extractor.
        """
        from ..kg_ingest import ingest_budgets

        if ctx:
            await ctx.info("Ingesting Firefly III budgets...")
        kwargs = json.loads(params_json) if params_json else {}
        resp = await run_blocking(client.list_budget, **kwargs)
        records = _records(resp)
        return {"listed": len(records), "ingested": ingest_budgets(records)}

    return None
