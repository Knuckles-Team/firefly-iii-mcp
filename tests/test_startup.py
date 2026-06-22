import importlib

import pytest


@pytest.mark.concept("FF-001")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:FF-001"""
    assert importlib.import_module("firefly_iii_mcp.mcp_server") is not None
