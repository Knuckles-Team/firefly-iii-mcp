#!/usr/bin/python

import logging
import sys
from typing import Any

from agent_utilities.base_utilities import get_logger
from agent_utilities.mcp_utilities import (
    create_mcp_server,
    load_config,
    register_tool_surface,
)

from . import mcp as tool_modules
from .api import ApiClientFireflyIii
from .auth import get_client

__version__ = "0.1.0"

logger = get_logger(name="MCP_Server")
logger.setLevel(logging.INFO)


def get_mcp_instance() -> tuple[Any, Any, Any]:
    """Initialize and return the Firefly III MCP MCP instance, args, and middlewares.

    The whole tool surface is wired by the shared ``register_tool_surface`` helper
    per ``MCP_TOOL_MODE`` (read from the XDG config): ``condensed`` (default,
    action-routed tools), ``verbose`` (one named 1:1 tool per API method), or
    ``both``. To add a domain, drop a ``register_<domain>_tools(mcp)`` into the
    ``mcp/`` package and re-export it from ``mcp/__init__.py`` — it is auto-discovered
    and gated by ``setting("<DOMAIN>TOOL", True)``; no edit here is needed. For
    fully-typed verbose tools, vendor an OpenAPI/Swagger spec under ``specs/`` and
    generate ``api/_operation_manifest.py``, then pass ``manifest=OPERATIONS`` below.
    """
    load_config()

    args, mcp, middlewares = create_mcp_server(
        name="Firefly III MCP MCP",
        version=__version__,
        instructions="Firefly III MCP MCP Server — condensed and verbose tool surfaces.",
    )

    register_tool_surface(
        mcp,
        service="firefly-iii-mcp",
        client_cls=ApiClientFireflyIii,
        get_client=get_client,
        tools_module=tool_modules,
    )

    for mw in middlewares:
        mcp.add_middleware(mw)

    return mcp, args, middlewares


def mcp_server():
    mcp, args, _ = get_mcp_instance()

    print(f"Firefly III MCP MCP v{__version__}", file=sys.stderr)
    print("\nStarting MCP Server", file=sys.stderr)
    print(f"  Transport: {args.transport.upper()}", file=sys.stderr)

    if args.transport == "stdio":
        mcp.run(transport="stdio")
    elif args.transport == "streamable-http":
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    elif args.transport == "sse":
        mcp.run(transport="sse", host=args.host, port=args.port)
    else:
        logger.error(f"Invalid transport: {args.transport}")
        sys.exit(1)


if __name__ == "__main__":
    mcp_server()
