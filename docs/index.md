# firefly-iii-mcp

Firefly III MCP **API + MCP Server + A2A Agent** for the agent-utilities ecosystem — a
typed, action-routed connector.

!!! info "Official documentation"
    This site is the canonical reference for `firefly-iii-mcp`, maintained alongside
    every release.

[![PyPI](https://img.shields.io/pypi/v/firefly-iii-mcp)](https://pypi.org/project/firefly-iii-mcp/)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
[![License](https://img.shields.io/pypi/l/firefly-iii-mcp)](https://github.com/Knuckles-Team/firefly-iii-mcp/blob/main/LICENSE)
[![GitHub](https://img.shields.io/badge/source-GitHub-181717?logo=github)](https://github.com/Knuckles-Team/firefly-iii-mcp)

## Overview

`firefly-iii-mcp` wraps the target service with typed, deterministic MCP tools and an
optional Pydantic-AI agent server.

The connector remains inactive when credentials are absent: configure
`FIREFLY_III_URL` and `FIREFLY_III_TOKEN` at runtime to connect it to an instance.
Endpoints, credentials, private trust, and finance records are never packaged values.

## Explore the documentation

<div class="grid cards" markdown>

- :material-rocket-launch: **[Installation](installation.md)** — pip, source, extras, and container targets.
- :material-shield-lock: **[Configuration](configuration.md)** — AgentConfig, verified TLS, secrets, and privacy.
- :material-server-network: **[Deployment](deployment.md)** — run the MCP and agent servers with runtime-injected configuration.
- :material-console: **[Usage](usage.md)** — the MCP tools, the Python client, and the CLI.
- :material-database-cog: **[Backing Platform](platform.md)** — connect an operator-managed Firefly III service.
- :material-sitemap: **[Overview](overview.md)** — the action-routed tool surface and architecture.
- :material-graph: **[Concepts](concepts.md)** — the CONCEPT ID registry.

</div>
