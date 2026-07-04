"""Native epistemic-graph ingestion for Firefly III records (typed graph nodes).

CONCEPT:AU-KG.ingest.enterprise-source-extractor. This is the record-source twin of
media-downloader's blob ingestion: the package natively pushes its personal-finance
data into the epistemic-graph knowledge graph as **typed OWL nodes** (``:Account``,
``:Transaction``, ``:Budget``, ``:Category``, ``:Bill``, ``:PiggyBank``, ``:Tag``,
``:Currency``) + links, using the lightweight engine client
(``GraphComputeEngine()._client`` + ``txn``) — the same fast client the blob
``MediaStore`` uses, NOT the heavy in-process ingestion engine.

The txn write path lives in the shared primitive
``agent_utilities.knowledge_graph.memory.native_ingest``; this module is a thin
Firefly-specific mapper over it. Both the shared primitive and this module are
dependency-/engine-guarded: with no agent-utilities KG stack or no reachable engine,
every entry point **no-ops** (returns ``None``), so the connector keeps working with
zero KG infrastructure. A self-contained txn fallback is kept here so ingestion works
even against an ``agent_utilities`` that does not yet ship the primitive. Nodes carry
the shared provenance (``domain``/``source``) and match the classes federated by
``firefly_iii_mcp.ontology``. Node ids follow ``firefly:<class>:<externalId>``.
"""

from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger("firefly_iii_mcp.kg")

_SOURCE = "firefly-iii-mcp"
_DOMAIN = "firefly"


def _shared() -> Any | None:
    """Return the shared ``native_ingest`` primitive module, or ``None``."""
    try:
        from agent_utilities.knowledge_graph.memory import (  # type: ignore
            native_ingest as ni,
        )

        return ni
    except Exception as e:  # noqa: BLE001 — primitive not yet installed
        logger.debug("native_ingest primitive unavailable: %s", e)
        return None


def _client() -> tuple[Any | None, str]:
    """Return ``(engine_client, graph_name)`` or ``(None, "")`` when unavailable.

    Self-contained fallback used when the shared primitive is absent.
    """
    try:
        from agent_utilities.knowledge_graph.core.graph_compute import (
            GraphComputeEngine,
        )
    except Exception as e:  # noqa: BLE001 — KG stack absent
        logger.debug("KG ingest unavailable (import): %s", e)
        return None, ""
    try:
        engine = GraphComputeEngine()
        client = getattr(engine, "_client", None)
        if client is None:
            return None, ""
        graph = getattr(engine, "graph_name", None) or "__commons__"
        return client, graph
    except Exception as e:  # noqa: BLE001 — engine unreachable
        logger.debug("KG ingest: engine unreachable: %s", e)
        return None, ""


def _write_nodes(
    client: Any,
    graph: str,
    nodes: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None,
) -> dict[str, int] | None:
    """Self-contained txn write path (fallback mirror of the shared primitive)."""
    nodes = [n for n in nodes if n.get("id")]
    if not nodes:
        return None
    try:
        txn = client.txn.begin(graph=graph)
        for node in nodes:
            props = {k: v for k, v in node.items() if k != "id" and v is not None}
            props.setdefault("source", _SOURCE)
            props.setdefault("domain", _DOMAIN)
            client.txn.add_node(txn, node["id"], props)
        committed = client.txn.commit(txn)
    except Exception as e:  # noqa: BLE001 — engine/txn failure is non-fatal
        logger.warning("KG ingest: txn failed: %s", e)
        return None
    if not committed:
        logger.warning("KG ingest: txn not committed (conflict)")
        return None

    edges = 0
    for rel in relationships or []:
        try:
            client.edges.add(
                rel["source"], rel["target"], {"type": rel.get("type", "RELATED")}
            )
            edges += 1
        except Exception as e:  # noqa: BLE001 — pure edge link, best-effort
            logger.debug("KG ingest: edge skipped: %s", e)

    logger.info("KG ingest: wrote %d nodes, %d edges", len(nodes), edges)
    return {"nodes": len(nodes), "edges": edges}


def ingest_entities(
    entities: list[dict[str, Any]],
    relationships: list[dict[str, Any]] | None = None,
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write typed nodes (+ edges) into epistemic-graph via the fast engine client.

    ``entities``: ``[{"id":..., "type":<owl:Class>, ...props}]``.
    ``relationships``: ``[{"source":id, "target":id, "type":rel}]``.
    Returns ``{"nodes":n, "edges":m}`` or ``None`` (no engine / failure; never raises).
    An injected ``client`` always takes the self-contained path (deterministic tests);
    otherwise the shared primitive is preferred, falling back to a local engine client.
    """
    entities = [e for e in (entities or []) if e.get("id")]
    if not entities:
        return None
    if client is None:
        ni = _shared()
        if ni is not None:
            return ni.ingest_entities(
                entities, relationships, source=source, domain=domain, graph=graph
            )
        client, graph = _client()
    if client is None:
        return None
    return _write_nodes(client, graph or "__commons__", entities, relationships)


def ingest_documents(
    docs: list[dict[str, Any]],
    *,
    source: str = _SOURCE,
    domain: str = _DOMAIN,
    client: Any | None = None,
    graph: str | None = None,
) -> dict[str, int] | None:
    """Write text records as ``:Document`` nodes (semantic-search fodder).

    Each doc: ``{"id":..., "text":..., "title"?:..., "source_uri"?:..., ...props}``.
    Returns ``{"nodes":n, "edges":0}`` or ``None``.
    """
    docs = [
        d for d in (docs or []) if d.get("id") and (d.get("text") or d.get("content"))
    ]
    if not docs:
        return None
    if client is None:
        ni = _shared()
        if ni is not None:
            return ni.ingest_documents(docs, source=source, domain=domain, graph=graph)
        client, graph = _client()
    if client is None:
        return None
    nodes: list[dict[str, Any]] = []
    for doc in docs:
        node = {k: v for k, v in doc.items() if k != "content" and v is not None}
        node["type"] = "Document"
        node["text"] = doc.get("text") or doc.get("content")
        nodes.append(node)
    return _write_nodes(client, graph or "__commons__", nodes, None)


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
                "type": "Account",
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
                    "type": "Currency",
                    "code": code,
                    "symbol": a.get("currency_symbol"),
                }
            )
            relationships.append(
                {
                    "source": f"firefly:account:{aid}",
                    "target": f"firefly:currency:{code}",
                    "type": "denominatedIn",
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
                "type": "Transaction",
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
                    "type": "sourceAccount",
                }
            )
        dst = split.get("destination_id")
        if dst:
            relationships.append(
                {
                    "source": f"firefly:transaction:{tid}",
                    "target": f"firefly:account:{dst}",
                    "type": "destinationAccount",
                }
            )
        bud = split.get("budget_id")
        if bud:
            relationships.append(
                {
                    "source": f"firefly:transaction:{tid}",
                    "target": f"firefly:budget:{bud}",
                    "type": "inBudget",
                }
            )
        cat = split.get("category_id")
        if cat:
            relationships.append(
                {
                    "source": f"firefly:transaction:{tid}",
                    "target": f"firefly:category:{cat}",
                    "type": "inCategory",
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
                "type": "Budget",
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
