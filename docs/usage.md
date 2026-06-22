# Usage — API / CLI / MCP

`firefly-iii-mcp` exposes the same capability three ways: as **MCP tools** an agent
calls, as a **Python API** you import, and as a **CLI**.

## As an MCP server

Once [deployed](deployment.md), the server registers consolidated, action-routed
tool modules. Each module is independently togglable with a `*TOOL` environment
flag.

## As a Python API

```python
from firefly_iii_mcp.auth import get_client

api = get_client()        # reads FIREFLY_III_URL / FIREFLY_III_TOKEN from the environment / .env
status = api.get_system_status()
```

## As a CLI

```bash
export FIREFLY_III_URL="http://localhost:8080"
export FIREFLY_III_TOKEN="your_token"
firefly-iii-mcp --transport stdio
```
