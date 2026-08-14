"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_accounts`` / ``ingest_transactions``
/ ``ingest_budgets`` seam with a fake ChangeEnvelope-capable engine client (no engine
required), asserting the committed nodes/edges and the Firefly record -> typed-node
mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.

The fake client mirrors agent-utilities' own sanctioned test double
(``agent-utilities/tests/knowledge_graph/test_native_ingest.py``) — the ``txn``-only
fake is retired; ``native_ingest`` now hard-requires an injected client exposing
``.changes``/``.nodes``/``.rdf``/``.supports()``. Unlike most fleet connectors,
``firefly_iii_mcp.kg_ingest`` is a **best-effort** surface (its MCP tools must never
raise when the KG stack is down), so it converts ``NativeIngestError`` into ``None``
rather than propagating it — those semantics are exercised explicitly below.
"""

from __future__ import annotations

from typing import Any

import msgpack
import pytest
from agent_utilities.knowledge_graph.core.session import GraphSession, use_session
from agent_utilities.models.company_brain import ActorType
from agent_utilities.security.brain_context import ActorContext, use_actor

from firefly_iii_mcp.kg_ingest import (
    ingest_accounts,
    ingest_budgets,
    ingest_entities,
    ingest_transactions,
)


@pytest.fixture(autouse=True)
def _governed_session():
    actor = ActorContext(
        actor_id="subject:opaque:synthetic",
        actor_type=ActorType.AUTOMATED_SERVICE,
        roles=(),
        tenant_id="tenant:opaque:synthetic",
        authenticated=True,
    )
    session = GraphSession(
        actor=actor,
        tenant=actor.tenant_id,
        scopes=frozenset({"kg:write"}),
        graph="graph:opaque:synthetic",
        policy_version="policy:opaque:synthetic",
        audience="epistemic-graph",
    )
    with use_actor(actor), use_session(session):
        yield


class _FakeNodes:
    def __init__(self) -> None:
        self.values: dict[str, dict[str, Any]] = {}

    def properties(self, node_id: str) -> dict[str, Any] | None:
        return self.values.get(node_id)

    def list(self) -> list[tuple[str, dict[str, Any]]]:
        return list(self.values.items())


class _FakeChanges:
    def __init__(self, nodes: _FakeNodes) -> None:
        self.nodes = nodes
        self.edges: list[tuple[str, str, dict[str, Any]]] = []
        self.applied: list[dict[str, Any]] = []
        self.records: dict[str, dict[str, Any]] = {}
        self.versions: dict[str, dict[str, Any]] = {}

    def get(self, envelope_id: str) -> dict[str, Any] | None:
        return self.records.get(envelope_id)

    def content_version(self, object_id: str) -> dict[str, Any] | None:
        return self.versions.get(object_id)

    def cursor(self, _source: str, _partition: str = "") -> None:
        return None

    def apply(self, envelope: dict[str, Any]) -> dict[str, Any]:
        self.applied.append(envelope)
        mutation = envelope["mutation"]
        for operation in mutation["operations"]:
            method = operation["method"]
            params = method["params"]
            properties = msgpack.unpackb(params["properties_msgpack"], raw=False)
            if method["method"] == "AddNode":
                self.nodes.values[params["node_id"]] = properties
            elif method["method"] == "AddEdge":
                self.edges.append(
                    (params["source_id"], params["target_id"], properties)
                )
        version = envelope["content_version"]
        self.versions[version["object_id"]] = version
        self.records[envelope["envelope_id"]] = envelope
        return {
            "batch_id": mutation["batch_id"],
            "replayed": False,
            "projection_pending": False,
        }


class _FakeRdf:
    def validate_shacl(self, _shapes: str, _data_graph: str) -> dict[str, Any]:
        return {"conforms": True, "results": []}


class _FakeClient:
    def __init__(self) -> None:
        self.nodes = _FakeNodes()
        self.changes = _FakeChanges(self.nodes)
        self.rdf = _FakeRdf()

    @staticmethod
    def supports(operation: str) -> bool:
        return operation == "ApplyChangeEnvelope"


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "node_type": "Account", "name": "checking"},
            {"id": "cur", "node_type": "Currency", "code": "USD"},
        ],
        [{"source": "a", "target": "cur", "relationship": "denominatedIn"}],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    assert set(c.nodes.values) == {"a", "cur"}
    # provenance is stamped
    assert c.nodes.values["a"]["source"] == "firefly-iii-mcp"
    assert c.nodes.values["a"]["domain"] == "firefly"
    assert c.changes.edges == [("a", "cur", {"relationship": "denominatedIn"})]


def test_ingest_accounts_maps_account_and_currency():
    c = _FakeClient()
    res = ingest_accounts(
        [
            {
                "id": "12",
                "attributes": {
                    "name": "Everyday Checking",
                    "type": "asset",
                    "account_role": "defaultAsset",
                    "current_balance": "1500.00",
                    "currency_code": "USD",
                    "currency_symbol": "$",
                },
            }
        ],
        client=c,
    )
    assert res == {"nodes": 2, "edges": 1}
    acct = c.nodes.values["firefly:account:12"]
    assert acct["node_type"] == "Account"
    assert acct["name"] == "Everyday Checking"
    assert acct["accountType"] == "asset"
    assert acct["externalToolId"] == "12"
    assert c.nodes.values["firefly:currency:USD"]["node_type"] == "Currency"
    assert c.changes.edges == [
        (
            "firefly:account:12",
            "firefly:currency:USD",
            {"relationship": "denominatedIn"},
        )
    ]


def test_ingest_transactions_maps_splits_and_links():
    c = _FakeClient()
    res = ingest_transactions(
        [
            {
                "id": "789",
                "attributes": {
                    "updated_at": "2026-02-14T10:00:00Z",
                    "transactions": [
                        {
                            "type": "withdrawal",
                            "description": "Groceries",
                            "amount": "42.50",
                            "currency_code": "USD",
                            "date": "2026-02-14",
                            "source_id": "12",
                            "destination_id": "30",
                            "budget_id": "3",
                            "category_id": "5",
                        }
                    ],
                },
            }
        ],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 4}
    txn = c.nodes.values["firefly:transaction:789"]
    assert txn["node_type"] == "Transaction"
    assert txn["transactionType"] == "withdrawal"
    assert txn["amount"] == "42.50"
    assert txn["splitCount"] == 1
    edge_types = {(s, d, p["relationship"]) for s, d, p in c.changes.edges}
    assert (
        "firefly:transaction:789",
        "firefly:account:12",
        "sourceAccount",
    ) in edge_types
    assert (
        "firefly:transaction:789",
        "firefly:account:30",
        "destinationAccount",
    ) in edge_types
    assert ("firefly:transaction:789", "firefly:budget:3", "inBudget") in edge_types
    assert ("firefly:transaction:789", "firefly:category:5", "inCategory") in edge_types


def test_ingest_budgets_maps_budget():
    c = _FakeClient()
    res = ingest_budgets(
        [{"id": "3", "attributes": {"name": "Groceries", "active": True}}],
        client=c,
    )
    assert res == {"nodes": 1, "edges": 0}
    bud = c.nodes.values["firefly:budget:3"]
    assert bud["node_type"] == "Budget"
    assert bud["name"] == "Groceries"
    assert bud["externalToolId"] == "3"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op (best-effort surface).
    assert ingest_entities([{"id": "a", "node_type": "Account"}]) is None


def test_ingest_rejects_retired_structural_alias_as_noop():
    # firefly_iii_mcp's tool surface is best-effort (never raises): a malformed
    # record (the retired ``type`` alias instead of canonical ``node_type``) is
    # reported back as a clean no-op rather than propagating NativeIngestError.
    c = _FakeClient()
    assert ingest_entities([{"id": "a", "type": "Account"}], client=c) is None
    assert c.changes.applied == []


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_accounts([], client=_FakeClient()) is None
    assert ingest_transactions([], client=_FakeClient()) is None
    assert ingest_budgets([], client=_FakeClient()) is None
