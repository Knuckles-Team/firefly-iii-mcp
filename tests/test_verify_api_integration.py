"""Characterize scripts/verify_api_integration.py's AST-based parity extraction.

This script is a contract-checker gate (API-to-MCP-action parity, no imports) rather
than a package module, so it is loaded by file path. Each helper is exercised against
synthetic ``api_client_*.py`` / ``mcp_*.py`` trees so the parity math (missing/unknown)
is pinned independently of the real Firefly III surface.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "verify_api_integration.py"
_spec = importlib.util.spec_from_file_location("verify_api_integration", _SCRIPT_PATH)
assert _spec and _spec.loader
verify_api_integration = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = verify_api_integration
_spec.loader.exec_module(verify_api_integration)

_public_api_methods = verify_api_integration._public_api_methods
_condensed_actions = verify_api_integration._condensed_actions


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_public_api_methods_collects_public_non_excluded_methods(tmp_path: Path):
    _write(
        tmp_path / "firefly_iii_mcp" / "api" / "api_client_accounts.py",
        "class ApiClientAccounts:\n"
        "    def list_accounts(self):\n"
        "        pass\n"
        "    def _private_helper(self):\n"
        "        pass\n"
        "    def close(self):\n"
        "        pass\n"
        "    async def async_list(self):\n"
        "        pass\n",
    )
    assert _public_api_methods(tmp_path) == {"list_accounts", "async_list"}


def test_public_api_methods_skips_base_and_composite_client_files(tmp_path: Path):
    _write(
        tmp_path / "firefly_iii_mcp" / "api" / "api_client_base.py",
        "class ApiClientBase:\n    def request(self):\n        pass\n",
    )
    _write(
        tmp_path / "firefly_iii_mcp" / "api" / "api_client_firefly_iii.py",
        "class ApiClientFireflyIii:\n    def anything(self):\n        pass\n",
    )
    assert _public_api_methods(tmp_path) == set()


def test_condensed_actions_collects_resolve_action_literal_set(tmp_path: Path):
    _write(
        tmp_path / "firefly_iii_mcp" / "mcp" / "mcp_accounts.py",
        "def handler(action):\n"
        "    resolve_action(action, {'list_accounts', 'get_account'})\n",
    )
    assert _condensed_actions(tmp_path) == {"list_accounts", "get_account"}


def test_condensed_actions_collects_client_attribute_calls(tmp_path: Path):
    _write(
        tmp_path / "firefly_iii_mcp" / "mcp" / "mcp_accounts.py",
        "def handler(client, api):\n"
        "    client.list_accounts()\n"
        "    api.get_account()\n"
        "    other.ignored()\n",
    )
    assert _condensed_actions(tmp_path) == {"list_accounts", "get_account"}


def test_condensed_actions_ignores_resolve_action_without_literal_collection(
    tmp_path: Path,
):
    _write(
        tmp_path / "firefly_iii_mcp" / "mcp" / "mcp_accounts.py",
        "def handler(action, allowed):\n"
        "    resolve_action(action, allowed)\n"
        "    resolve_action(action)\n",
    )
    assert _condensed_actions(tmp_path) == set()


def test_parity_flags_known_bad_missing_action(tmp_path: Path):
    """Plant a known-bad input: a public API method absent from condensed actions."""
    _write(
        tmp_path / "firefly_iii_mcp" / "api" / "api_client_accounts.py",
        "class ApiClientAccounts:\n"
        "    def list_accounts(self):\n"
        "        pass\n"
        "    def delete_account(self):\n"
        "        pass\n",
    )
    _write(
        tmp_path / "firefly_iii_mcp" / "mcp" / "mcp_accounts.py",
        "def handler(client):\n    client.list_accounts()\n",
    )
    methods = _public_api_methods(tmp_path)
    actions = _condensed_actions(tmp_path)
    assert methods - actions == {"delete_account"}  # FAIL: gate must flag this

    # Remove the bad input (add the missing action) -> gate goes clean.
    _write(
        tmp_path / "firefly_iii_mcp" / "mcp" / "mcp_accounts.py",
        "def handler(client):\n    client.list_accounts()\n    client.delete_account()\n",
    )
    actions = _condensed_actions(tmp_path)
    assert methods - actions == set()  # PASS: clean parity
