# CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION — Requirements

Governing specification: [spec.md](spec.md).

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION-R001` | **Governed HTTP.** The connector must reach Firefly III only through the SDK governed HTTP client in `firefly_iii_mcp/api/api_client_base.py`. It must not import `requests`. Caller chain: any Firefly tool (`firefly_iii_mcp/mcp/mcp_*.py`) -> `get_client` (`firefly_iii_mcp/auth.py` line 141) -> `ApiClientBase` (`firefly_iii_mcp/api/api_client_base.py` line 50) -> `create_http_client` (line 62) from `scion_sdk.http.client`. Shape: `ApiClientBase.__init__` builds `self.session` with `create_http_client(HttpClientOptions(...))` and imports no `requests`; `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` asserts an `httpx.Client` and scans the package source. | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |
