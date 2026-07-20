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

api = get_client()
try:
    status = api.get_about()
finally:
    api.close()
```

## As a CLI

Inject `FIREFLY_III_URL` and, when delegation is disabled, `FIREFLY_III_TOKEN`
through the runtime configuration boundary, then run:

```bash
firefly-iii-mcp --transport stdio
```

Use the packaged `firefly-iii-finance-operations` skill for read-before-write
workflow, double-entry conventions, mutation approval, and governed source-sync rules.
