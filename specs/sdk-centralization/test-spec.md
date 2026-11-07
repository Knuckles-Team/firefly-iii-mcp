# CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION — Verification plan

Governing specification: [spec.md](spec.md).

| Requirement | Verification target |
|---|---|
| `CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION-R001` | `tests/test_sdk_centralization.py::test_api_client_uses_sdk_http_client` must observe an SDK client and no `requests` import. |

## Adoption of scion-sdk 0.10.0 (`CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION-R002`)

| Requirement | Test | Observation |
|---|---|---|
| `CONN-FIREFLY-III-MCP-SDK-CENTRALIZATION-R002` | `tests/test_scion_sdk_0_10_imports.py::test_every_scion_sdk_import_resolves_on_the_pinned_release` | Every `scion_sdk` import resolves on the pinned release; a removed path fails the test. |
