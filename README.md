# Firefly III MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/firefly-iii-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/firefly-iii-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/firefly-iii-mcp)
![PyPI - License](https://img.shields.io/pypi/l/firefly-iii-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/firefly-iii-mcp)

*Version: 1.0.1*

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
| `about_operations` | `ABOUTTOOL` | Manage Firefly III `about` operations. CONCEPT:FF-OS.config.ff |
| `accounts_operations` | `ACCOUNTSTOOL` | Manage Firefly III `accounts` operations. CONCEPT:FF-OS.config.ff |
| `attachments_operations` | `ATTACHMENTSTOOL` | Manage Firefly III `attachments` operations. CONCEPT:FF-OS.config.ff |
| `autocomplete_operations` | `AUTOCOMPLETETOOL` | Manage Firefly III `autocomplete` operations. CONCEPT:FF-OS.config.ff |
| `available_budgets_operations` | `AVAILABLE_BUDGETSTOOL` | Manage Firefly III `available_budgets` operations. CONCEPT:FF-OS.config.ff |
| `bills_operations` | `BILLSTOOL` | Manage Firefly III `bills` operations. CONCEPT:FF-OS.config.ff |
| `budgets_operations` | `BUDGETSTOOL` | Manage Firefly III `budgets` operations. CONCEPT:FF-OS.config.ff |
| `categories_operations` | `CATEGORIESTOOL` | Manage Firefly III `categories` operations. CONCEPT:FF-OS.config.ff |
| `charts_operations` | `CHARTSTOOL` | Manage Firefly III `charts` operations. CONCEPT:FF-OS.config.ff |
| `configuration_operations` | `CONFIGURATIONTOOL` | Manage Firefly III `configuration` operations. CONCEPT:FF-OS.config.ff |
| `currencies_operations` | `CURRENCIESTOOL` | Manage Firefly III `currencies` operations. CONCEPT:FF-OS.config.ff |
| `currency_exchange_rates_operations` | `CURRENCY_EXCHANGE_RATESTOOL` | Manage Firefly III `currency_exchange_rates` operations. CONCEPT:FF-OS.config.ff |
| `data_operations` | `DATATOOL` | Manage Firefly III `data` operations. CONCEPT:FF-OS.config.ff |
| `insight_operations` | `INSIGHTTOOL` | Manage Firefly III `insight` operations. CONCEPT:FF-OS.config.ff |
| `links_operations` | `LINKSTOOL` | Manage Firefly III `links` operations. CONCEPT:FF-OS.config.ff |
| `object_groups_operations` | `OBJECT_GROUPSTOOL` | Manage Firefly III `object_groups` operations. CONCEPT:FF-OS.config.ff |
| `piggy_banks_operations` | `PIGGY_BANKSTOOL` | Manage Firefly III `piggy_banks` operations. CONCEPT:FF-OS.config.ff |
| `preferences_operations` | `PREFERENCESTOOL` | Manage Firefly III `preferences` operations. CONCEPT:FF-OS.config.ff |
| `recurrences_operations` | `RECURRENCESTOOL` | Manage Firefly III `recurrences` operations. CONCEPT:FF-OS.config.ff |
| `rule_groups_operations` | `RULE_GROUPSTOOL` | Manage Firefly III `rule_groups` operations. CONCEPT:FF-OS.config.ff |
| `rules_operations` | `RULESTOOL` | Manage Firefly III `rules` operations. CONCEPT:FF-OS.config.ff |
| `search_operations` | `SEARCHTOOL` | Manage Firefly III `search` operations. CONCEPT:FF-OS.config.ff |
| `summary_operations` | `SUMMARYTOOL` | Manage Firefly III `summary` operations. CONCEPT:FF-OS.config.ff |
| `tags_operations` | `TAGSTOOL` | Manage Firefly III `tags` operations. CONCEPT:FF-OS.config.ff |
| `transactions_operations` | `TRANSACTIONSTOOL` | Manage Firefly III `transactions` operations. CONCEPT:FF-OS.config.ff |
| `user_groups_operations` | `USER_GROUPSTOOL` | Manage Firefly III `user_groups` operations. CONCEPT:FF-OS.config.ff |
| `users_operations` | `USERSTOOL` | Manage Firefly III `users` operations. CONCEPT:FF-OS.config.ff |
| `webhooks_operations` | `WEBHOOKSTOOL` | Manage Firefly III `webhooks` operations. CONCEPT:FF-OS.config.ff |

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

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the slim `[mcp]` extra.** All examples install `firefly-iii-mcp[mcp]` — the
> MCP-server extra that pulls only the FastMCP / FastAPI tooling (`agent-utilities[mcp]`).
> It deliberately **excludes** the heavy agent runtime (`pydantic-ai`, the epistemic-graph
> engine, `dspy`, `llama-index`), so `uvx` / container installs are far smaller. Use the
> full `[agent]` extra only when you need the integrated Pydantic AI agent.

#### stdio Transport (local IDEs — Cursor, Claude Desktop, VS Code)

```json
{
  "mcpServers": {
    "firefly-iii-mcp": {
      "command": "uvx",
      "args": [
        "--from",
        "firefly-iii-mcp[mcp]",
        "firefly-iii-mcp"
      ],
      "env": {
        "MCP_TOOL_MODE": "condensed",
        "ABOUTTOOL": "True",
        "ACCOUNTSTOOL": "True",
        "ATTACHMENTSTOOL": "True",
        "AUTOCOMPLETETOOL": "True",
        "AVAILABLE_BUDGETSTOOL": "True",
        "BILLSTOOL": "True",
        "BUDGETSTOOL": "True",
        "CATEGORIESTOOL": "True",
        "CHARTSTOOL": "True",
        "CONFIGURATIONTOOL": "True",
        "CURRENCIESTOOL": "True",
        "CURRENCY_EXCHANGE_RATESTOOL": "True",
        "DATATOOL": "True",
        "FIREFLY_III_TOKEN": "your_token_here",
        "FIREFLY_III_URL": "http://localhost:8080",
        "INSIGHTTOOL": "True",
        "LINKSTOOL": "True",
        "OBJECT_GROUPSTOOL": "True",
        "PIGGY_BANKSTOOL": "True",
        "PREFERENCESTOOL": "True",
        "RECURRENCESTOOL": "True",
        "RULESTOOL": "True",
        "RULE_GROUPSTOOL": "True",
        "SEARCHTOOL": "True",
        "SUMMARYTOOL": "True",
        "TAGSTOOL": "True",
        "TRANSACTIONSTOOL": "True",
        "USERSTOOL": "True",
        "USER_GROUPSTOOL": "True",
        "WEBHOOKSTOOL": "True"
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
      "args": [
        "--from",
        "firefly-iii-mcp[mcp]",
        "firefly-iii-mcp",
        "--transport",
        "streamable-http",
        "--port",
        "8000"
      ],
      "env": {
        "TRANSPORT": "streamable-http",
        "HOST": "0.0.0.0",
        "PORT": "8000",
        "MCP_TOOL_MODE": "condensed",
        "ABOUTTOOL": "True",
        "ACCOUNTSTOOL": "True",
        "ATTACHMENTSTOOL": "True",
        "AUTOCOMPLETETOOL": "True",
        "AVAILABLE_BUDGETSTOOL": "True",
        "BILLSTOOL": "True",
        "BUDGETSTOOL": "True",
        "CATEGORIESTOOL": "True",
        "CHARTSTOOL": "True",
        "CONFIGURATIONTOOL": "True",
        "CURRENCIESTOOL": "True",
        "CURRENCY_EXCHANGE_RATESTOOL": "True",
        "DATATOOL": "True",
        "FIREFLY_III_TOKEN": "your_token_here",
        "FIREFLY_III_URL": "http://localhost:8080",
        "INSIGHTTOOL": "True",
        "LINKSTOOL": "True",
        "OBJECT_GROUPSTOOL": "True",
        "PIGGY_BANKSTOOL": "True",
        "PREFERENCESTOOL": "True",
        "RECURRENCESTOOL": "True",
        "RULESTOOL": "True",
        "RULE_GROUPSTOOL": "True",
        "SEARCHTOOL": "True",
        "SUMMARYTOOL": "True",
        "TAGSTOOL": "True",
        "TRANSACTIONSTOOL": "True",
        "USERSTOOL": "True",
        "USER_GROUPSTOOL": "True",
        "WEBHOOKSTOOL": "True"
      }
    }
  }
}
```

Alternatively, connect to a pre-deployed Streamable-HTTP instance by `url`:

```json
{
  "mcpServers": {
    "firefly-iii-mcp": {
      "url": "http://localhost:8000/firefly-iii-mcp/mcp"
    }
  }
}
```

Deploying the Streamable-HTTP server via Docker:

```bash
docker run -d \
  --name firefly-iii-mcp-mcp \
  -p 8000:8000 \
  -e TRANSPORT=streamable-http \
  -e HOST=0.0.0.0 \
  -e PORT=8000 \
  -e MCP_TOOL_MODE=condensed \
  -e ABOUTTOOL=True \
  -e ACCOUNTSTOOL=True \
  -e ATTACHMENTSTOOL=True \
  -e AUTOCOMPLETETOOL=True \
  -e AVAILABLE_BUDGETSTOOL=True \
  -e BILLSTOOL=True \
  -e BUDGETSTOOL=True \
  -e CATEGORIESTOOL=True \
  -e CHARTSTOOL=True \
  -e CONFIGURATIONTOOL=True \
  -e CURRENCIESTOOL=True \
  -e CURRENCY_EXCHANGE_RATESTOOL=True \
  -e DATATOOL=True \
  -e FIREFLY_III_TOKEN=your_token_here \
  -e FIREFLY_III_URL=http://localhost:8080 \
  -e INSIGHTTOOL=True \
  -e LINKSTOOL=True \
  -e OBJECT_GROUPSTOOL=True \
  -e PIGGY_BANKSTOOL=True \
  -e PREFERENCESTOOL=True \
  -e RECURRENCESTOOL=True \
  -e RULESTOOL=True \
  -e RULE_GROUPSTOOL=True \
  -e SEARCHTOOL=True \
  -e SUMMARYTOOL=True \
  -e TAGSTOOL=True \
  -e TRANSACTIONSTOOL=True \
  -e USERSTOOL=True \
  -e USER_GROUPSTOOL=True \
  -e WEBHOOKSTOOL=True \
  knucklessg1/firefly-iii-mcp:mcp
```

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

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


<!-- BEGIN agent-os-genesis-deploy (generated; do not edit between markers) -->

## Deploy with `agent-os-genesis`

This package can be provisioned for you — skill-guided — by the **`agent-os-genesis`**
universal skill (its *single-package deploy mode*): it picks your install method, seeds
secrets to OpenBao/Vault (or `.env`), trusts your enterprise CA, registers the MCP
server, and verifies it — the same machinery that stands up the whole Agent OS, narrowed
to just this package. Ask your agent to **"deploy `firefly-iii-mcp` with agent-os-genesis"**.

| Install mode | Command |
|------|---------|
| Bare-metal, prod (PyPI) | `uvx firefly-iii-mcp` · or `uv tool install firefly-iii-mcp` |
| Bare-metal, dev (editable) | `uv pip install -e ".[all]"` · or `pip install -e ".[all]"` |
| Container, prod | deploy `knucklessg1/firefly-iii-mcp:latest` via docker-compose / swarm / podman / podman-compose / kubernetes |
| Container, dev (editable) | deploy `docker/compose.dev.yml` (source-mounted at `/src`; edits live on restart) |

Secrets are read-existing + seeded via `vault_sync` — you are only prompted for what's missing.

<!-- END agent-os-genesis-deploy -->
