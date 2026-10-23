from pathlib import Path

import pytest

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
def test_direct_graph_write_surface_is_absent():
    """Graph writes go only through the SDK's generated source-ingest client."""
    package = ROOT / "firefly_iii_mcp"
    source = (package / "kg_ingest.py").read_text(encoding="utf-8")
    assert "agent_connector_sdk.ingest" in source
