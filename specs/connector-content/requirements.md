# CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT — Requirements

Governing spec: [spec.md](spec.md).

Each row is one requirement. A row names the file it touches and the test that proves it. The generator sets each row's state in `status.json`.

| ID | Requirement | Acceptance |
|---|---|---|
| `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R001` | **Default content.** `pyproject.toml` declares `firefly-iii-mcp` as the single `scion_sdk.connector` entry point. The server lists the packaged `skill://` and `ontology://` resources and the packaged prompts with no `content=` argument. Proving test: `tests/test_default_content_surfaces.py`. Caller chain: the `firefly-iii-mcp = scion_sdk.cli:serve` console script in `pyproject.toml` -> entry point `firefly_iii_mcp:connector` (`firefly_iii_mcp/__init__.py` line 60) -> SDK-built server serving the packaged `firefly_iii_mcp/skills` and `ontology` content. Shape: content is the packaged `firefly_iii_mcp/skills/` and `firefly_iii_mcp/ontology/` directories (no `prompts/` directory today); copy the `fastmcp.Client` listing pattern of immich-api `tests/test_default_content_surfaces.py` and build the server through `scion_sdk.connector.build_server`. | `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Planned test: `tests/test_default_content_surfaces.py::test_default_content_surfaces`. |
