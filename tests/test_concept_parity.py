from pathlib import Path

import pytest

CONCEPTS_DOC = Path(__file__).resolve().parents[1] / "docs" / "concepts.md"


@pytest.mark.concept("FF-001")
def test_concepts_doc_exists():
    """Concept registry doc exists. CONCEPT:FF-001"""
    assert CONCEPTS_DOC.is_file()


@pytest.mark.concept("FF-001")
def test_eco_bridge_present():
    """ECO-4.0 bridge concept is referenced. CONCEPT:FF-001"""
    assert "ECO-4.0" in CONCEPTS_DOC.read_text(encoding="utf-8")


@pytest.mark.concept("FF-001")
def test_prefix_registered():
    """Project concept prefix is registered. CONCEPT:FF-001"""
    assert "CONCEPT:FF-" in CONCEPTS_DOC.read_text(encoding="utf-8")
