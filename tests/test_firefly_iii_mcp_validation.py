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
    """The provider exposes one comprehensive current skill."""
    skills = sorted((ROOT / "firefly_iii_mcp" / "skills").glob("*/SKILL.md"))
    assert [path.parent.name for path in skills] == ["firefly-iii-finance-operations"]
    assert (skills[0].parent / "agents" / "openai.yaml").is_file()


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
    assert not (connectors / "tool_schema_fingerprints.json").exists()
    assert not (ROOT / "connector_manifest.yml").exists()


@pytest.mark.concept("FF-OS.config.ff")
def test_provider_entry_points_prove_package_ownership():
    """Every provider leg resolves to a data package in the owning wheel."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    entry_points = project["project"]["entry-points"]
    assert entry_points["agent_utilities.skill_providers"] == {
        "firefly-iii-mcp": "firefly_iii_mcp.skills"
    }
    assert entry_points["agent_utilities.ontology_providers"] == {
        "firefly-iii-mcp": "firefly_iii_mcp.ontology"
    }
    assert entry_points["agent_utilities.source_connector_providers"] == {
        "firefly-iii-mcp": "firefly_iii_mcp.connectors"
    }
    assert entry_points["agent_utilities.prompt_providers"] == {
        "firefly-iii-mcp": "firefly_iii_mcp.prompts"
    }


@pytest.mark.concept("FF-OS.config.ff")
def test_direct_graph_write_surface_is_absent():
    """Finance records can enter the graph only through central source sync."""
    package = ROOT / "firefly_iii_mcp"
    assert not (package / "kg_ingest.py").exists()
    assert not (package / "mcp" / "mcp_kg.py").exists()
