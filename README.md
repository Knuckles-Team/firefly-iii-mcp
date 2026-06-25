# Firefly III MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/firefly-iii-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/firefly-iii-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/firefly-iii-mcp)
![PyPI - License](https://img.shields.io/pypi/l/firefly-iii-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/firefly-iii-mcp)

*Version: 0.1.0*

> **Documentation** — Installation, deployment, usage across the API, CLI, and MCP
> interfaces, the integrated A2A agent server, and guidance for provisioning the
> backing platform are maintained in the
> [official documentation](https://knuckles-team.github.io/firefly-iii-mcp/).

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Available MCP Tools](#available-mcp-tools)
- [Installation](#installation)
- [Usage](#usage)
- [MCP](#mcp)
- [Documentation](#documentation)

---

## Overview

**Firefly III MCP MCP Server + A2A Agent**

Firefly III API + MCP Server + A2A Agent — personal finance manager

This repository is actively maintained - Contributions are welcome!

## Key Features

- **Action-routed MCP tools** — each domain is exposed as a single MCP tool that routes
  to many underlying operations via an `action` argument, keeping the tool surface small.
- **Three interfaces, one package** — use it as a Python **API client**, an **MCP server**
  (`stdio` / `streamable-http` / `sse`), or a Pydantic-AI **A2A agent**.
- **`agent-utilities` native** — built on the shared framework (auth, action router,
  telemetry, governance) for fleet consistency.
- **Per-tool toggles** — enable or disable each tool domain with environment switches.
- **Enterprise-ready** — OTEL/Langfuse telemetry and optional Eunomia access governance.

## Available MCP Tools

Each tool is **action-routed**: pass an `action` and a JSON `params_json` payload. Tool
domains can be toggled on or off with the listed environment variable. The table below is
**auto-generated from the live server** by the `mcp-readme-table` pre-commit hook
(`python -m agent_utilities.mcp.readme_tools`) — do not edit it by hand.

<!-- MCP-TOOLS-TABLE:START -->

| MCP Tool | Toggle Env Var | Description |
|----------|----------------|-------------|
| `about_operations` | `ABOUTTOOL` | Manage Firefly III `about` operations. CONCEPT:FF-001 |
| `accounts_operations` | `ACCOUNTSTOOL` | Manage Firefly III `accounts` operations. CONCEPT:FF-001 |
| `attachments_operations` | `ATTACHMENTSTOOL` | Manage Firefly III `attachments` operations. CONCEPT:FF-001 |
| `autocomplete_operations` | `AUTOCOMPLETETOOL` | Manage Firefly III `autocomplete` operations. CONCEPT:FF-001 |
| `available_budgets_operations` | `AVAILABLE_BUDGETSTOOL` | Manage Firefly III `available_budgets` operations. CONCEPT:FF-001 |
| `bills_operations` | `BILLSTOOL` | Manage Firefly III `bills` operations. CONCEPT:FF-001 |
| `budgets_operations` | `BUDGETSTOOL` | Manage Firefly III `budgets` operations. CONCEPT:FF-001 |
| `categories_operations` | `CATEGORIESTOOL` | Manage Firefly III `categories` operations. CONCEPT:FF-001 |
| `charts_operations` | `CHARTSTOOL` | Manage Firefly III `charts` operations. CONCEPT:FF-001 |
| `configuration_operations` | `CONFIGURATIONTOOL` | Manage Firefly III `configuration` operations. CONCEPT:FF-001 |
| `currencies_operations` | `CURRENCIESTOOL` | Manage Firefly III `currencies` operations. CONCEPT:FF-001 |
| `currency_exchange_rates_operations` | `CURRENCY_EXCHANGE_RATESTOOL` | Manage Firefly III `currency_exchange_rates` operations. CONCEPT:FF-001 |
| `data_operations` | `DATATOOL` | Manage Firefly III `data` operations. CONCEPT:FF-001 |
| `insight_operations` | `INSIGHTTOOL` | Manage Firefly III `insight` operations. CONCEPT:FF-001 |
| `links_operations` | `LINKSTOOL` | Manage Firefly III `links` operations. CONCEPT:FF-001 |
| `object_groups_operations` | `OBJECT_GROUPSTOOL` | Manage Firefly III `object_groups` operations. CONCEPT:FF-001 |
| `piggy_banks_operations` | `PIGGY_BANKSTOOL` | Manage Firefly III `piggy_banks` operations. CONCEPT:FF-001 |
| `preferences_operations` | `PREFERENCESTOOL` | Manage Firefly III `preferences` operations. CONCEPT:FF-001 |
| `recurrences_operations` | `RECURRENCESTOOL` | Manage Firefly III `recurrences` operations. CONCEPT:FF-001 |
| `rule_groups_operations` | `RULE_GROUPSTOOL` | Manage Firefly III `rule_groups` operations. CONCEPT:FF-001 |
| `rules_operations` | `RULESTOOL` | Manage Firefly III `rules` operations. CONCEPT:FF-001 |
| `search_operations` | `SEARCHTOOL` | Manage Firefly III `search` operations. CONCEPT:FF-001 |
| `summary_operations` | `SUMMARYTOOL` | Manage Firefly III `summary` operations. CONCEPT:FF-001 |
| `tags_operations` | `TAGSTOOL` | Manage Firefly III `tags` operations. CONCEPT:FF-001 |
| `transactions_operations` | `TRANSACTIONSTOOL` | Manage Firefly III `transactions` operations. CONCEPT:FF-001 |
| `user_groups_operations` | `USER_GROUPSTOOL` | Manage Firefly III `user_groups` operations. CONCEPT:FF-001 |
| `users_operations` | `USERSTOOL` | Manage Firefly III `users` operations. CONCEPT:FF-001 |
| `webhooks_operations` | `WEBHOOKSTOOL` | Manage Firefly III `webhooks` operations. CONCEPT:FF-001 |

_28 action-routed tools (default `MCP_TOOL_MODE=condensed`). Each is enabled unless its toggle is set false; set `MCP_TOOL_MODE=verbose` (or `both`) for the 1:1 per-operation surface. Auto-generated — do not edit._
<!-- MCP-TOOLS-TABLE:END -->

## Installation

Pick the extra that matches what you want to run:

| Extra | Installs | Use when |
|-------|----------|----------|
| `firefly-iii-mcp[mcp]` | Slim MCP server only (`agent-utilities[mcp]` — FastMCP/FastAPI) | You only run the **MCP server** (smallest install / image) |
| `firefly-iii-mcp[agent]` | Full agent runtime (`agent-utilities[agent,logfire]` — Pydantic AI + the epistemic-graph engine) | You run the **integrated agent** |
| `firefly-iii-mcp[all]` | Everything (`mcp` + `agent` + `logfire`) | Development / both surfaces |

### Install with `uvx` (no install — run on demand)

```bash
uvx --from "firefly-iii-mcp[mcp]" firefly-iii-mcp      # MCP server
uvx --from "firefly-iii-mcp[agent]" firefly-iii-agent  # A2A agent server
```

### Install with `pip` / `uv`

```bash
# MCP server only (recommended for tool hosting — slim deps)
uv pip install "firefly-iii-mcp[mcp]"

# Full agent runtime (Pydantic AI + epistemic-graph engine)
uv pip install "firefly-iii-mcp[agent]"

# Everything (development)
uv pip install "firefly-iii-mcp[all]"      # or: python -m pip install "firefly-iii-mcp[all]"
```

### Container images (`:mcp` vs `:agent`)

One multi-stage `docker/Dockerfile` builds two right-sized images, selected by `--target`:

| Image tag | Build target | Contents | Entrypoint |
|-----------|--------------|----------|------------|
| `knucklessg1/firefly-iii-mcp:mcp` | `--target mcp` | `firefly-iii-mcp[mcp]` — **slim**, no engine/`pydantic-ai`/`dspy`/`llama-index`/`tree-sitter` | `firefly-iii-mcp` |
| `knucklessg1/firefly-iii-mcp:latest` | `--target agent` (default) | `firefly-iii-mcp[agent]` — **full** agent runtime + epistemic-graph engine | `firefly-iii-agent` |

```bash
docker build --target mcp   -t knucklessg1/firefly-iii-mcp:mcp    docker/   # slim MCP server
docker build --target agent -t knucklessg1/firefly-iii-mcp:latest docker/   # full agent
```

`docker/mcp.compose.yml` runs the slim `:mcp` server; `docker/agent.compose.yml` runs the
agent (`:latest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

The **full agent** (`[agent]` / `:latest`) embeds the **epistemic-graph** engine (pulled in
transitively via `agent-utilities[agent]`). For production — or to share one knowledge graph
across multiple agents — run **epistemic-graph as its own database container** and point the
agent at it instead of embedding it. Deployment recipes (single-node + Raft HA), connection
config, and the full database architecture (with diagrams) are documented in the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).
The slim `[mcp]` server does **not** require the database.

### Console scripts

After installation the following entry points are available on your `PATH`:

| Command | Description |
|---------|-------------|
| `firefly-iii-mcp` | Launch the MCP server |
| `firefly-iii-agent` | Launch the A2A agent server |

## Usage

### As a Python API client

```python
from firefly_iii_mcp.auth import get_client

client = get_client()
status = client.get_system_status()
print(status)
```

### As an MCP server (CLI)

```bash
# Local stdio (for IDEs)
firefly-iii-mcp

# Networked streamable-http
firefly-iii-mcp --transport streamable-http --host 0.0.0.0 --port 8000
```

### Calling an MCP tool

Tools are action-routed — pass an `action` plus a JSON `params_json` string:

```json
{
  "tool": "system_operations",
  "arguments": {
    "action": "status",
    "params_json": "{}"
  }
}
```

## MCP

> **Install the slim `[mcp]` extra.** All MCP examples below install
> `firefly-iii-mcp[mcp]` — the MCP-server extra that pulls only the FastMCP /
> FastAPI tooling (`agent-utilities[mcp]`). It deliberately **excludes** the heavy
> agent runtime (the epistemic-graph engine, `pydantic-ai`, `dspy`, `llama-index`,
> `tree-sitter`), so `uvx`/container installs are dramatically smaller and faster.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

### Using as an MCP Server

The MCP Server can be run in `stdio` (local), `streamable-http` (networked), or
`sse` mode.

#### Environment Variables

Every variable the server reads. A copy-paste template lives in [`.env.example`](.env.example).

**Connection & Credentials**

| Variable | Description | Default |
|----------|-------------|---------|
| `FIREFLY_III_URL` | Firefly III base URL | `http://localhost:8080` |
| `FIREFLY_III_TOKEN` | API token / Personal Access Token | — |
| `FIREFLY_III_SSL_VERIFY` | TLS certificate verification | `True` |

**MCP server / transport**

| Variable | Description | Default |
|----------|-------------|---------|
| `TRANSPORT` | `stdio`, `streamable-http`, or `sse` | `stdio` |
| `HOST` | Bind host (HTTP transports) | `0.0.0.0` |
| `PORT` | Bind port (HTTP transports) | `8000` |
| `MCP_TOOL_MODE` | Tool surface: `condensed`, `verbose`, or `both` | `condensed` |

**Telemetry & governance**

| Variable | Description | Default |
|----------|-------------|---------|
| `ENABLE_OTEL` | Enable OpenTelemetry / Langfuse export | `True` |
| `EUNOMIA_TYPE` | Authorization mode: `none`, `embedded`, `remote` | `none` |
| `EUNOMIA_POLICY_FILE` | Embedded policy file | `mcp_policies.json` |
| `EUNOMIA_REMOTE_URL` | Remote Eunomia server URL | — |

**Tool toggles** — each action-routed tool domain can be disabled via its toggle env var
(set to `false`); the full list is in the [Available MCP Tools](#available-mcp-tools) table
above (e.g. `ACCOUNTSTOOL`, `TRANSACTIONSTOOL`, `BUDGETSTOOL`).

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "firefly-iii-mcp": {
      "command": "uvx",
      "args": ["--from", "firefly-iii-mcp[mcp]", "firefly-iii-mcp"],
      "env": {
        "FIREFLY_III_URL": "https://service.example.com",
        "FIREFLY_III_TOKEN": "your_token"
      }
    }
  }
}
```

#### Streamable-HTTP Transport (networked / production)

```json
{
  "mcpServers": {
    "firefly-iii-mcp": {
      "command": "uvx",
      "args": ["--from", "firefly-iii-mcp[mcp]", "firefly-iii-mcp", "--transport", "streamable-http", "--port", "8000"],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "FIREFLY_III_URL": "https://service.example.com",
        "FIREFLY_III_TOKEN": "your_token"
      }
    }
  }
}
```

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`firefly-iii-mcp` can also run as a **local container** (Docker / Podman / `uv`) or be
consumed from a **remote deployment**. The
[Deployment guide](https://knuckles-team.github.io/firefly-iii-mcp/deployment/) has full,
copy-paste `mcp_config.json` for all four transports — **stdio**, **streamable-http**,
**local container / uv**, and **remote URL**:

- **Local container / uv** — launch the server from `mcp_config.json` via `uvx`,
  `docker run`, or `podman run`, or point at a local streamable-http container by `url`.
- **Remote URL** — connect to a server deployed behind Caddy at
  `http://firefly-iii-mcp.arpa/mcp` using the `"url"` key.
<!-- END GENERATED: additional-deployment-options -->

## Install Python Package

```bash
python -m pip install firefly-iii-mcp
```

## Documentation

Full documentation is published to the GitHub Pages site and mirrored under `docs/`:

- [Documentation site](https://knuckles-team.github.io/firefly-iii-mcp/)
- [Overview](docs/overview.md)
- [Installation](docs/installation.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)
