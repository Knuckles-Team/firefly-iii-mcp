# CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION — Verification plan

Governing specification: [spec.md](spec.md).

| Requirement | Verification target |
|---|---|
| `CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION-R001` | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |
