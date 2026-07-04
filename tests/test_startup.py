import importlib

import pytest


@pytest.mark.concept("FF-OS.config.ff")
def test_mcp_server_module_importable():
    """MCP server module imports cleanly at startup. CONCEPT:FF-OS.config.ff"""
    assert importlib.import_module("firefly_iii_mcp.mcp_server") is not None
