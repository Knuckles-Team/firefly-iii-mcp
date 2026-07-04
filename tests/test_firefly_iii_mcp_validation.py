import pytest

from firefly_iii_mcp.mcp_server import get_mcp_instance


@pytest.mark.concept("FF-OS.config.ff")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its tool domains registered.

    CONCEPT:FF-OS.config.ff
    """
    monkeypatch.setattr("sys.argv", ["firefly-iii-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None
