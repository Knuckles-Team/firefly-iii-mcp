"""Native epistemic-graph typed-node ingestion — Wire-First coverage.

Exercises the real ``ingest_entities`` / ``ingest_accounts`` / ``ingest_transactions``
/ ``ingest_budgets`` seam against a fake SDK transport (no engine required),
asserting the submitted records/relationships and the Firefly record -> typed-node
mapping. CONCEPT:AU-KG.ingest.enterprise-source-extractor.

Unlike most fleet connectors, ``firefly_iii_mcp.kg_ingest`` is a **best-effort**
surface (its MCP tools must never raise when the KG stack is down), so it converts
``IngestError``/``IngestUnavailableError`` into ``None`` rather than propagating it —
those semantics are exercised explicitly below.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest
from agent_connector_sdk.ingest import KnowledgeIngest

from firefly_iii_mcp.kg_ingest import (
    ingest_accounts,
    ingest_budgets,
    ingest_entities,
    ingest_transactions,
)


class _FakeTransport:
    def __init__(self) -> None:
        self.requests: list[Any] = []

    async def source_status(self, connector: str, stream: str) -> Any:
        return SimpleNamespace(accepted_checkpoint=None)

    async def submit(self, request: Any) -> Any:
        self.requests.append(request)
        return SimpleNamespace(
            affected_count=len(request.records),
            relationship_count=len(request.relationships),
        )

    async def store_blob(self, data: Any) -> Any:
        raise AssertionError("this connector's ingestion carries no media")


@pytest.fixture
def ingest():
    transport = _FakeTransport()
    return KnowledgeIngest(transport, loop=None), transport


async def test_ingest_entities_writes_nodes_and_edges(ingest):
    service, transport = ingest
    res = await ingest_entities(
        [
            {"id": "a", "node_type": "Account", "name": "checking"},
            {"id": "cur", "node_type": "Currency", "code": "USD"},
        ],
        [{"source": "a", "target": "cur", "relationship": "denominatedIn"}],
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    record_ids = {r.record_id for r in transport.requests[0].records}
    assert record_ids == {"a", "cur"}
    rel = transport.requests[0].relationships[0]
    assert rel.source.record_id == "a"
    assert rel.target.record_id == "cur"


async def test_ingest_accounts_maps_account_and_currency(ingest):
    service, transport = ingest
    res = await ingest_accounts(
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
        ingest=service,
    )
    assert res == {"nodes": 2, "edges": 1}
    records = {r.record_id: r for r in transport.requests[0].records}
    acct = records["firefly:account:12"]
    assert acct.payload["name"] == "Everyday Checking"
    assert acct.payload["accountType"] == "asset"
    assert acct.payload["externalToolId"] == "12"
    assert "firefly:currency:USD" in records
    rel = transport.requests[0].relationships[0]
    assert rel.source.record_id == "firefly:account:12"
    assert rel.target.record_id == "firefly:currency:USD"


async def test_ingest_transactions_maps_splits_and_links(ingest):
    service, transport = ingest
    res = await ingest_transactions(
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
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 4}
    txn = transport.requests[0].records[0]
    assert txn.record_id == "firefly:transaction:789"
    assert txn.payload["transactionType"] == "withdrawal"
    assert txn.payload["amount"] == "42.50"
    assert txn.payload["splitCount"] == 1
    edge_targets = {r.target.record_id for r in transport.requests[0].relationships}
    assert edge_targets == {
        "firefly:account:12",
        "firefly:account:30",
        "firefly:budget:3",
        "firefly:category:5",
    }


async def test_ingest_transactions_skips_records_without_an_id(ingest):
    service, _transport = ingest
    res = await ingest_transactions(
        [{"attributes": {"transactions": [{"description": "no id"}]}}],
        ingest=service,
    )
    assert res is None


async def test_ingest_transactions_falls_back_to_flat_record_without_splits(ingest):
    service, transport = ingest
    res = await ingest_transactions(
        [
            {
                "id": "42",
                "attributes": {
                    "description": "Flat record, no transactions list",
                    "type": "deposit",
                    "amount": "10.00",
                },
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    txn = transport.requests[0].records[0]
    assert txn.payload["description"] == "Flat record, no transactions list"
    assert txn.payload["splitCount"] == 1


async def test_ingest_transactions_only_links_present_fields(ingest):
    service, transport = ingest
    res = await ingest_transactions(
        [
            {
                "id": "5",
                "attributes": {
                    "transactions": [
                        {
                            "description": "Only a source account",
                            "source_id": "12",
                        }
                    ],
                },
            }
        ],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 1}
    rel = transport.requests[0].relationships[0]
    assert rel.source.record_id == "firefly:transaction:5"
    assert rel.target.record_id == "firefly:account:12"


async def test_ingest_budgets_maps_budget(ingest):
    service, transport = ingest
    res = await ingest_budgets(
        [{"id": "3", "attributes": {"name": "Groceries", "active": True}}],
        ingest=service,
    )
    assert res == {"nodes": 1, "edges": 0}
    bud = transport.requests[0].records[0]
    assert bud.record_id == "firefly:budget:3"
    assert bud.payload["name"] == "Groceries"
    assert bud.payload["externalToolId"] == "3"


async def test_ingest_noops_without_engine():
    # No injected ingest + no reachable engine -> clean no-op (best-effort surface).
    assert await ingest_entities([{"id": "a", "node_type": "Account"}]) is None


async def test_ingest_rejects_retired_structural_alias_as_noop(ingest):
    # firefly_iii_mcp's tool surface is best-effort (never raises): a malformed
    # record (the retired ``type`` alias instead of canonical ``node_type``) is
    # reported back as a clean no-op rather than propagating IngestError.
    service, transport = ingest
    assert await ingest_entities([{"id": "a", "type": "Account"}], ingest=service) is None
    assert transport.requests == []


async def test_ingest_empty_is_noop(ingest):
    service, _transport = ingest
    assert await ingest_entities([], ingest=service) is None
    assert await ingest_accounts([], ingest=service) is None
    assert await ingest_transactions([], ingest=service) is None
    assert await ingest_budgets([], ingest=service) is None
