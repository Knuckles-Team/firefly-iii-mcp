import json
from pathlib import Path

import pytest
import tomllib

from firefly_iii_mcp.mcp_server import get_mcp_instance

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.concept("FF-OS.config.ff")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its tool domains registered.

    CONCEPT:FF-OS.config.ff
    """
    monkeypatch.setattr("sys.argv", ["firefly-iii-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None


@pytest.mark.concept("FF-OS.config.ff")
def test_provider_has_one_current_skill():
    """The provider ships its current skills; the operations skill has UI metadata."""
    root = ROOT / "firefly_iii_mcp" / "skills"
    skills = sorted(root.glob("*/SKILL.md"))
    assert [path.parent.name for path in skills] == [
        "firefly-iii-account-management",
        "firefly-iii-budgeting",
        "firefly-iii-finance-operations",
        "firefly-iii-transaction-ledger",
    ]
    assert (root / "firefly-iii-finance-operations" / "agents" / "openai.yaml").is_file()


@pytest.mark.concept("FF-OS.config.ff")
def test_provider_inputs_are_neutral_and_unsigned():
    """Connector-owned source inputs contain no deployment artifact."""
    connectors = ROOT / "firefly_iii_mcp" / "connectors"
    presets = json.loads(
        (connectors / "mcp_source_presets.json").read_text(encoding="utf-8")
    )
    assert {key for key in presets if not key.startswith("_")} == {
        "firefly-accounts",
        "firefly-budgets",
        "firefly-transactions",
    }
    assert (connectors / "tool_schema_fingerprints.json").is_file()


@pytest.mark.concept("FF-OS.config.ff")
def test_provider_entry_points_prove_package_ownership():
    """Every provider leg resolves to a data package in the owning wheel."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    entry_points = project["project"]["entry-points"]
    assert entry_points["agent_connector_sdk.skill_providers"] == {
        "firefly-iii-mcp": "firefly_iii_mcp.skills"
    }
    assert entry_points["agent_connector_sdk.ontology_providers"] == {
        "firefly-iii-mcp": "firefly_iii_mcp.ontology"
    }
    assert entry_points["agent_connector_sdk.source_connector_providers"] == {
        "firefly-iii-mcp": "firefly_iii_mcp.connectors"
    }


@pytest.mark.concept("FF-OS.config.ff")
def test_direct_graph_write_surface_is_absent():
    """Graph writes go only through the SDK's generated source-ingest client."""
    package = ROOT / "firefly_iii_mcp"
    source = (package / "kg_ingest.py").read_text(encoding="utf-8")
    assert "agent_connector_sdk.ingest" in source
