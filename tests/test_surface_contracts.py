"""Connector surface: contracts, links, prompts and ontology roll-up (CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R002)."""

from pathlib import Path

import pytest

PACKAGE = Path(__file__).resolve().parents[1] / "firefly_iii_mcp"

pytestmark = pytest.mark.spec("CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R002")


def test_served_surface_has_no_contract_link_or_prompt_gap() -> None:
    from scion_sdk.testing.surface_check import surface_check

    assert surface_check("firefly_iii_mcp") == []


def test_every_ontology_class_rolls_up_to_core() -> None:
    from scion_sdk.testing.ontology_rollup import orphan_classes

    ttl = PACKAGE / "ontology" / "firefly.ttl"
    assert "owl:imports" not in ttl.read_text(encoding="utf-8")
    assert orphan_classes(ttl) == set()
