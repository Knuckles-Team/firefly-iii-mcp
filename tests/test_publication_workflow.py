"""Keep shared publication and Pages contracts explicit in this connector."""

from __future__ import annotations

import json
import re
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _workflow(name: str):
    return yaml.safe_load((ROOT / ".github/workflows" / name).read_text())


def _actions_on(workflow: dict):
    # PyYAML's YAML 1.1 reader represents the Actions ``on`` key as True.
    return workflow["on"] if "on" in workflow else workflow[True]


def test_pages_publishes_spec_dashboard_and_supports_manual_refresh():

    config = json.loads((ROOT / ".config/spec-dashboard.json").read_text())
    assert config == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }


def test_legacy_docs_publisher_is_removed_and_release_flags_remain_canonical():
    assert not (ROOT / ".github/workflows/docs.yml").exists()


def test_development_skill_has_real_delivery_contract_and_actual_tests():
    skill = ROOT / "firefly_iii_mcp/skills/firefly-iii-mcp-development/SKILL.md"
    content = skill.read_text()

    assert "name: firefly-iii-mcp-development" in content
    assert "## Rapid delivery: the 5-minute contract" in content
    for test_path in (
        "tests/test_publication_workflow.py",
        "tests/test_startup.py",
        "tests/test_firefly_iii_mcp_validation.py",
        "tests/test_auth.py",
        "tests/test_api_wrapper.py",
    ):
        assert test_path in content
        assert (ROOT / test_path).exists()
    assert "FIREFLY_III_URL" in content
    assert "agent_connector_sdk" in content
    assert "condensed/verbose" in content


def test_packaged_skill_and_version_lock_are_coherent():
    project = tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]
    version = project["version"]
    lock = (ROOT / "uv.lock").read_text()
    assert re.search(
        rf'^name = "firefly-iii-mcp"\nversion = "{re.escape(version)}"$',
        lock,
        re.MULTILINE,
    )
    package_data = tomllib.loads((ROOT / "pyproject.toml").read_text())["tool"][
        "setuptools"
    ]["package-data"]
    assert "skills/**" in package_data["firefly_iii_mcp"]
    assert (
        ROOT / "firefly_iii_mcp/skills/firefly-iii-mcp-development/SKILL.md"
    ).is_file()
