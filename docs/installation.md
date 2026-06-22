# Installation

`firefly-iii-mcp` is a standard Python package and a prebuilt container image.

## Requirements

- **Python 3.11 – 3.14**.
- A reachable target service instance and access token.

## From PyPI (recommended)

```bash
pip install firefly-iii-mcp
```

### Optional extras

| Extra | Install | Pulls in |
|---|---|---|
| `mcp` | `pip install "firefly-iii-mcp[mcp]"` | FastMCP MCP-server runtime (`agent-utilities[mcp]`) |
| `agent` | `pip install "firefly-iii-mcp[agent]"` | Pydantic-AI agent + Logfire tracing |
| `all` | `pip install "firefly-iii-mcp[all]"` | Everything above |

## From source

```bash
git clone https://github.com/Knuckles-Team/firefly-iii-mcp.git
cd firefly-iii-mcp
pip install -e ".[all]"
```

## Docker

```bash
docker pull knucklessg1/firefly-iii-mcp:latest
```
