# Firefly III MCP
## CLI or API | MCP | Agent

![PyPI - Version](https://img.shields.io/pypi/v/firefly-iii-mcp)
![MCP Server](https://badge.mcpx.dev?type=server 'MCP Server')
![PyPI - Downloads](https://img.shields.io/pypi/dd/firefly-iii-mcp)
![GitHub Repo stars](https://img.shields.io/github/stars/Knuckles-Team/firefly-iii-mcp)
![PyPI - License](https://img.shields.io/pypi/l/firefly-iii-mcp)
![GitHub last commit (by committer)](https://img.shields.io/github/last-commit/Knuckles-Team/firefly-iii-mcp)

*Version: 2.0.0*

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
- **Verified transport profiles** — outbound HTTP uses AgentConfig-backed TLS trust;
  peer and hostname verification cannot be disabled by this connector.
- **Governed graph inputs** — ships one comprehensive skill, a neutral ontology, and
  source presets without packaging an instance URL, custom schema, or credential.
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
| `firefly-iii-mcp[mcp]` | MCP server (`agent-utilities[mcp]`) plus the mandatory full epistemic-graph base runtime | You run the **MCP server** without the agent UI/runtime |
| `firefly-iii-mcp[agent]` | Current agent runtime (`agent-utilities[agent-runtime,logfire]`) | You run the **integrated agent** |
| `firefly-iii-mcp[all]` | MCP + agent runtime + Logfire | Development or both surfaces |

### Install with `uvx` (no install — run on demand)

```bash
uvx --from "firefly-iii-mcp[mcp]" firefly-iii-mcp      # MCP server
uvx --from "firefly-iii-mcp[agent]" firefly-iii-agent  # A2A agent server
```

### Install with `pip` / `uv`

```bash
# MCP server only (recommended for tool hosting)
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
| `firefly-iii-mcp:mcp` | `--target mcp` | MCP server plus the mandatory full epistemic-graph base dependency | `firefly-iii-mcp` |
| `firefly-iii-mcp@sha256:<digest>` | `--target agent` (default) | MCP dependencies plus the current Pydantic-AI agent runtime | `firefly-iii-agent` |

```bash
docker build --target mcp -t firefly-iii-mcp:mcp -f docker/Dockerfile .
docker build --target agent -t firefly-iii-mcp:agent-local -f docker/Dockerfile .
```

`docker/mcp.compose.yml` runs the MCP-only `:mcp` server; `docker/agent.compose.yml` runs the
agent (`immutable agent digest`) with a co-located `:mcp` sidecar.

### Knowledge-graph database (`epistemic-graph`)

Every install receives `epistemic-graph[full]` through the current Agent Utilities base
dependency. The connector does not open an insecure engine listener or silently select a
machine-specific engine. Deployment topology and identity are resolved by AgentConfig. For a
shared production authority, follow the
[epistemic-graph deployment guide](https://knuckles-team.github.io/epistemic-graph/deployment/).

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
try:
    print(client.get_about())
finally:
    client.close()
```

### As an MCP server (CLI)

```bash
# Local stdio (for IDEs)
firefly-iii-mcp

# Networked streamable-http
firefly-iii-mcp --transport streamable-http --host 127.0.0.1 --port 8000
```

### Calling an MCP tool

Tools are action-routed — pass an `action` plus a JSON `params_json` string:

```json
{
  "tool": "about_operations",
  "arguments": {
    "action": "get_about",
    "params_json": "{}"
  }
}
```

## MCP

> **Install the MCP-only `[mcp]` extra.** All MCP examples below install
> `firefly-iii-mcp[mcp]` — the MCP-server extra that adds the FastMCP / FastAPI
> tooling (`agent-utilities[mcp]`) to the shared base. The integrated Pydantic-AI
> and UI runtime is separate, while full epistemic-graph remains mandatory.
> Use the full `[agent]` extra only when you need the integrated Pydantic AI agent
> (see [Installation](#installation)).

### MCP Configuration Examples

<!-- MCP-CONFIG-EXAMPLES:START -->

> **Install the connector-focused `[mcp]` extra.** Examples use `firefly-iii-mcp[mcp]` to add
> FastMCP / FastAPI through `agent-utilities[mcp]`; the required Agent Utilities core
> still carries `epistemic-graph[full]`. The `[agent-runtime]` extra additionally
> enables model orchestration.

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
        "MCP_TOOL_MODE": "intent",
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

Runtime references require an alias-aware launcher such as GraphOS. Other
launchers must omit those entries and inject the resolved values through their
own runtime secret boundary.

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
        "HOST": "127.0.0.1",
        "PORT": "8000",
        "MCP_TOOL_MODE": "intent",
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

Run a reviewed container image as a least-privilege stdio child (no
listener or published port):

```bash
docker run -i --rm \
  --read-only \
  --cap-drop=ALL \
  --security-opt=no-new-privileges \
  --pids-limit=256 \
  --tmpfs /tmp:rw,noexec,nosuid,nodev,size=64m \
  -e TRANSPORT=stdio \
  -e MCP_TOOL_MODE=intent \
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
  registry.example.invalid/firefly-iii-mcp@sha256:<digest> firefly-iii-mcp
```

For containerized network HTTP, supply an authenticated TLS ingress (or
direct server TLS), exact `MCP_ALLOWED_HOSTS`, and an exact trusted-proxy
CIDR policy through the operator-owned deployment profile. The generator
does not emit an unauthenticated non-loopback listener.

_Auto-generated from the code-read env surface (`MCP_TOOL_MODE` + package vars) — do not edit._
<!-- MCP-CONFIG-EXAMPLES:END -->

<!-- BEGIN GENERATED: additional-deployment-options -->
### Additional Deployment Options

`firefly-iii-mcp` can run as a local stdio process or container, or behind a remote
network boundary. The
[Deployment guide](https://knuckles-team.github.io/firefly-iii-mcp/deployment/) carries
the detailed transport contract.

- **Local container** — launch a reviewed immutable image as a least-privilege
  stdio child with no listener or published port.
- **Remote URL** — connect through an operator-supplied authenticated HTTPS
  ingress. Keep its URL, outbound identity references, trust profile, and exact
  `MCP_ALLOWED_HOSTS` in `AgentConfig`.
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
- [Configuration, Trust, and Privacy](docs/configuration.md)
- [Usage](docs/usage.md)
- [Deployment](docs/deployment.md)
- [Platform](docs/platform.md)
- [Concept Registry](docs/concepts.md)


<!-- BEGIN agent-utilities-deployment (generated; do not edit between markers) -->

## Deploy with `agent-utilities-deployment`

Provision this package with the consolidated **`agent-utilities-deployment`**
workflow. It selects an installed-package, editable-source, or immutable-container
path; records only runtime secret and TLS-profile references in `AgentConfig`; and
runs doctor, registration, policy, observability, and rollback gates. Ask your agent
to **"deploy `firefly-iii-mcp` with agent-utilities-deployment"**.

| Install mode | Command |
|------|---------|
| Installed package | `uv tool install "firefly-iii-mcp[mcp]"`, then run `firefly-iii-mcp` |
| Editable source | `uv pip install -e ".[agent]"`, then run `firefly-iii-mcp` |
| Immutable container | deploy `registry.example.invalid/firefly-iii-mcp@sha256:<digest>` through the operator-selected orchestrator |

The repository embeds no deployment profile, credential value, certificate path, or
environment-specific endpoint. Supply those at runtime through `AgentConfig` and the
configured secret provider.

<!-- END agent-utilities-deployment -->

<!-- GOVERNED-CAPABILITY:START -->
## Governed capability contract

This package owns the complete release-generated schema-v2 capability bundle:
`connector_manifest.yml`, exact local MCP schema fingerprints, the neutral finance
ontology, SHACL shapes, source mappings and fixtures, the migration ledger, and an
offline source attestation. Release tooling derives and signs these artifacts from the
current sources; they are not hand-authored and do not claim external-live
certification.

Runtime endpoints, credentials, certificate trust, identity, tenant/ACL policy,
retention, and observability destinations are deployment inputs and are never packaged
values. See [Configuration, trust, and privacy](docs/configuration.md) before enabling
a network transport, GraphOS delegation, source synchronization, or trace export.
<!-- GOVERNED-CAPABILITY:END -->
