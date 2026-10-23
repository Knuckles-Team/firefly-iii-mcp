# CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT — Design and implementation plan

Governing spec: [spec.md](spec.md).

## Architecture

`pyproject.toml` declares `firefly-iii-mcp` as the connector identity. `create_mcp_server` resolves the packaged content of `firefly_iii_mcp` from it.
