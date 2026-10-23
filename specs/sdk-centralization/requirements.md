# CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION — Requirements

Governing specification: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION-R001` | **Governed HTTP.** The connector must reach Firefly III only through the SDK governed HTTP client in `firefly_iii_mcp/api/api_client_base.py`. It must not import `requests`. | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |
