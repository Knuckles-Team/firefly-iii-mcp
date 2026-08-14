"""Native epistemic-graph ingestion for Firefly III records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the package natively pushes its personal-finance
data into the ONE epistemic-graph knowledge graph as **typed OWL nodes**
(``:Account``, ``:Transaction``, ``:Budget``, ``:Category``, ``:Bill``, ``:PiggyBank``,
``:Tag``, ``:Currency``) plus links, through the required
``agent_utilities.knowledge_graph.memory.native_ingest`` authority — the one connector
write path; there is no self-contained fallback transaction here.

The MCP tool surface exposes these as best-effort tools that must never raise on an
unreachable/misconfigured KG stack, so ``ingest_entities``/``ingest_documents`` stay
**best-effort**: they return ``None`` (never raise) for empty input or when the shared
primitive reports :class:`NativeIngestError` (no reachable engine, or a malformed
record). Node ids follow ``firefly:<class>:<externalId>`` and each ``node_type``
matches a class federated by ``firefly_iii_mcp.ontology``.
"""

from __future__ import annotations

import logging
from typing import Any

from agent_utilities.knowledge_graph.memory.native_ingest import (
    NativeIngestError,
    ingest_documents as _native_ingest_documents,
    ingest_entities as _native_ingest_entities,
)

logger = logging.getLogger("firefly_iii_mcp.kg")

_SOURCE = "firefly-iii-mcp"
_DOMAIN = "firefly"


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed OWL nodes (+ edges) into epistemic-graph. Best-effort, never raises.

    ``entities``: ``[{"id":..., "node_type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "relationship":<link>}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (empty input / no reachable engine /
    malformed record). ``client``/``graph`` may be injected (tests); otherwise the
    process-owned governed authority is resolved on demand.
    """
    if not entities:
        return None
    try:
        return _native_ingest_entities(
            entities,
            relationships,
            source=source,
            domain=domain,
            client=client,
            graph=graph,
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder). Best-effort.

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    docs = [
        d for d in (docs or []) if d.get("id") and (d.get("text") or d.get("content"))
    ]
    if not docs:
        return None
    try:
        return _native_ingest_documents(
            docs, source=source, domain=domain, client=client, graph=graph
        )
    except NativeIngestError as exc:
        logger.debug("KG ingest unavailable/failed: %s", exc)
        return None


# --- Firefly-specific record → typed-node mappers -------------------------------


def _attrs(record: dict[str, Any]) -> tuple[str | None, dict[str, Any]]:
    """Unwrap a Firefly JSON:API resource ``{"id":.., "attributes":{..}}``.

    Tolerates already-flattened records (returns them as-is with their ``id``).
    """
    if not isinstance(record, dict):
        return None, {}
    rid = record.get("id")
    attrs = record.get("attributes")
    if isinstance(attrs, dict):
        return (str(rid) if rid is not None else None), attrs
    return (str(rid) if rid is not None else None), record


def ingest_accounts(
    accounts: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Firefly account records → ``:Account`` nodes (+ ``:Currency`` links)."""
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for rec in accounts or []:
        aid, a = _attrs(rec)
        if aid is None:
            continue
        entities.append(
            {
                "id": f"firefly:account:{aid}",
                "node_type": "Account",
                "name": a.get("name"),
                "accountRole": a.get("account_role") or a.get("type"),
                "accountType": a.get("type"),
                "currentBalance": a.get("current_balance"),
                "iban": a.get("iban"),
                "active": a.get("active"),
                "currencyCode": a.get("currency_code"),
                "updated_at": a.get("updated_at"),
                "externalToolId": aid,
            }
        )
        code = a.get("currency_code")
        if code:
            entities.append(
                {
                    "id": f"firefly:currency:{code}",
                    "node_type": "Currency",
                    "code": code,
                    "symbol": a.get("currency_symbol"),
                }
            )
            relationships.append(
                {
                    "source": f"firefly:account:{aid}",
                    "target": f"firefly:currency:{code}",
                    "relationship": "denominatedIn",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_transactions(
    transactions: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Firefly transaction groups → ``:Transaction`` nodes and their links.

    A Firefly transaction group holds one or more splits (journals) under
    ``attributes.transactions``. The first split supplies the summary fields and the
    source/destination account, budget and category links.
    """
    entities: list[dict[str, Any]] = []
    relationships: list[dict[str, Any]] = []
    for rec in transactions or []:
        tid, a = _attrs(rec)
        if tid is None:
            continue
        splits = a.get("transactions")
        split = splits[0] if isinstance(splits, list) and splits else a
        entities.append(
            {
                "id": f"firefly:transaction:{tid}",
                "node_type": "Transaction",
                "description": split.get("description"),
                "transactionType": split.get("type"),
                "amount": split.get("amount"),
                "currencyCode": split.get("currency_code"),
                "date": split.get("date"),
                "splitCount": len(splits) if isinstance(splits, list) else 1,
                "updated_at": a.get("updated_at"),
                "externalToolId": tid,
            }
        )
        src = split.get("source_id")
        if src:
            relationships.append(
                {
                    "source": f"firefly:transaction:{tid}",
                    "target": f"firefly:account:{src}",
                    "relationship": "sourceAccount",
                }
            )
        dst = split.get("destination_id")
        if dst:
            relationships.append(
                {
                    "source": f"firefly:transaction:{tid}",
                    "target": f"firefly:account:{dst}",
                    "relationship": "destinationAccount",
                }
            )
        bud = split.get("budget_id")
        if bud:
            relationships.append(
                {
                    "source": f"firefly:transaction:{tid}",
                    "target": f"firefly:budget:{bud}",
                    "relationship": "inBudget",
                }
            )
        cat = split.get("category_id")
        if cat:
            relationships.append(
                {
                    "source": f"firefly:transaction:{tid}",
                    "target": f"firefly:category:{cat}",
                    "relationship": "inCategory",
                }
            )
    return ingest_entities(entities, relationships, client=client, graph=graph)


def ingest_budgets(
    budgets: list[dict[str, Any]],
    *,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Map Firefly budget records → ``:Budget`` nodes."""
    entities: list[dict[str, Any]] = []
    for rec in budgets or []:
        bid, a = _attrs(rec)
        if bid is None:
            continue
        entities.append(
            {
                "id": f"firefly:budget:{bid}",
                "node_type": "Budget",
                "name": a.get("name"),
                "active": a.get("active"),
                "autoBudgetType": a.get("auto_budget_type"),
                "autoBudgetAmount": a.get("auto_budget_amount"),
                "currencyCode": a.get("currency_code"),
                "updated_at": a.get("updated_at"),
                "externalToolId": bid,
            }
        )
    return ingest_entities(entities, client=client, graph=graph)
