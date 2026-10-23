"""CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION-R001."""

from pathlib import Path

import httpx

from firefly_iii_mcp.api import ApiClientBase


def test_api_client_uses_sdk_http_client():
    client = ApiClientBase(base_url="https://firefly.example", token="t")
    assert isinstance(client.session, httpx.Client)
    root = Path(__file__).resolve().parents[1] / "firefly_iii_mcp"
    for source in root.rglob("*.py"):
        assert "import requests" not in source.read_text(), source
