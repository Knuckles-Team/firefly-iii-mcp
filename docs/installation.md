# Installation

`firefly-iii-mcp` is a standard Python package with MCP and agent container targets.

## Requirements

- **Python 3.11 – 3.14**.
- A runtime-configured Firefly III HTTPS endpoint and delegated or fixed credential.

## From PyPI (recommended)

```bash
pip install firefly-iii-mcp
```

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "firefly-iii-mcp[mcp]"` | MCP-server runtime plus the mandatory `epistemic-graph[full]` base dependency |
| `agent` | `pip install "firefly-iii-mcp[agent]"` | Current Pydantic-AI agent runtime + Logfire tracing |
| `all` | `pip install "firefly-iii-mcp[all]"` | Everything above |

## From source

```bash
git clone https://github.com/Knuckles-Team/firefly-iii-mcp.git
cd firefly-iii-mcp
pip install -e ".[all]"
```

## Container

```bash
docker build --target agent -t firefly-iii-mcp:agent-local -f docker/Dockerfile .
```

Inject endpoints, credentials, trust, and model settings through the runtime
orchestrator; do not add them to the image.
