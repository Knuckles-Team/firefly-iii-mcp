"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_accounts`` / ``ingest_transactions``
/ ``ingest_budgets`` seam with a fake engine client (no engine required), asserting
the txn add_node/commit + edge calls and the Firefly record → typed-node mapping.
CONCEPT:AU-KG.ingest.enterprise-source-extractor.
"""

from __future__ import annotations

from firefly_iii_mcp.kg_ingest import (
    ingest_accounts,
    ingest_budgets,
    ingest_entities,
    ingest_transactions,
)


class _FakeTxn:
    def __init__(self):
        self.nodes = {}
        self.committed = False

    def begin(self, graph=None):
        self.graph = graph
        return "txn-1"

    def add_node(self, txn, node_id, props):
        self.nodes[node_id] = props

    def commit(self, txn):
        self.committed = True
        return True


class _FakeEdges:
    def __init__(self):
        self.edges = []

    def add(self, src, dst, props):
        self.edges.append((src, dst, props))


class _FakeClient:
    def __init__(self):
        self.txn = _FakeTxn()
        self.edges = _FakeEdges()


def test_ingest_entities_writes_nodes_and_edges():
    c = _FakeClient()
    res = ingest_entities(
        [
            {"id": "a", "type": "Account", "name": "checking"},
            {"id": "cur", "type": "Currency", "code": "USD"},
        ],
        [{"source": "a", "target": "cur", "type": "denominatedIn"}],
        client=c,
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    assert c.txn.committed is True
    assert set(c.txn.nodes) == {"a", "cur"}
    # provenance is stamped
    assert c.txn.nodes["a"]["source"] == "firefly-iii-mcp"
    assert c.txn.nodes["a"]["domain"] == "firefly"
    assert c.edges.edges == [("a", "cur", {"type": "denominatedIn"})]


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
        graph="__commons__",
    )
    assert res == {"nodes": 2, "edges": 1}
    acct = c.txn.nodes["firefly:account:12"]
    assert acct["type"] == "Account"
    assert acct["name"] == "Everyday Checking"
    assert acct["accountType"] == "asset"
    assert acct["externalToolId"] == "12"
    assert c.txn.nodes["firefly:currency:USD"]["type"] == "Currency"
    assert c.edges.edges == [
        ("firefly:account:12", "firefly:currency:USD", {"type": "denominatedIn"})
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 4}
    txn = c.txn.nodes["firefly:transaction:789"]
    assert txn["type"] == "Transaction"
    assert txn["transactionType"] == "withdrawal"
    assert txn["amount"] == "42.50"
    assert txn["splitCount"] == 1
    edge_types = {(s, d, p["type"]) for s, d, p in c.edges.edges}
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
        graph="__commons__",
    )
    assert res == {"nodes": 1, "edges": 0}
    bud = c.txn.nodes["firefly:budget:3"]
    assert bud["type"] == "Budget"
    assert bud["name"] == "Groceries"
    assert bud["externalToolId"] == "3"


def test_ingest_noops_without_engine():
    # No injected client + no reachable engine -> clean no-op.
    assert ingest_entities([{"id": "a", "type": "Account"}]) is None


def test_ingest_empty_is_noop():
    assert ingest_entities([], client=_FakeClient()) is None
    assert ingest_accounts([], client=_FakeClient()) is None
    assert ingest_transactions([], client=_FakeClient()) is None
    assert ingest_budgets([], client=_FakeClient()) is None
