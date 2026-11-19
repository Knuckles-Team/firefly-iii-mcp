# CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT — The connector serves its packaged content

Owner: firefly-iii-mcp. Cross-repo IDs: `SCION-CONNECTOR-CONTROL-R071`, `SCION-CONNECTOR-CONTROL-R073`.

## Purpose and user stories

The `firefly-iii-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

## Why a new spec

The specs of this repository were read; none owns this capability. This spec states it for this connector only.

## Scope and interfaces

In scope: the rows of [requirements.md](requirements.md). Out of scope: the SDK modules and the engine, which own the shared capabilities.

## User Scenarios & Testing

### User Story 1 - The connector serves its packaged content (Priority: P1)

The `firefly-iii-mcp` server serves its packaged skills, prompts and ontology to any client, with no wiring of its own.

**Acceptance Scenarios**:

1. **Given** the connector is configured, **When** the behaviour of row `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R001` (default content) is exercised, **Then** `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt.

### User Story 2 - The connector surface is complete (Priority: P2)

Agents rely on `firefly-iii-mcp` declaring its whole surface: an ontology that rolls up to the core ontology, and tool-use contracts, links and prompts that name every typed tool.

**Acceptance Scenarios**:

1. **Given** the connector is built from the default branch, **When** the behaviour of row `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R002` (surface completeness) is exercised, **Then** every ontology class reaches a core class, and every served tool is in a contract, a link and an agent prompt.

### Edge Cases

- If `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R001` is not met, its proving test fails: default content.
- If `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R002` is not met, its proving test fails: surface completeness.

## Requirements

- **FR-001**: Default content. Rows: `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R001`.
- **FR-002**: Surface completeness. Rows: `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R002`.

## Success Criteria

- **SC-001**: `resources/list` includes `skill://` and `ontology://`; `prompts/list` includes each packaged prompt. Rows: `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R001`.
- **SC-002**: The surface audit reports no gap for the ontology, contracts, links and prompts. Rows: `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R002`.

## Assumptions

- The external system is reachable with operator-supplied credentials.
- The SDK and engine contracts the rows cite are at the floors declared in `pyproject.toml`.

## Traceability

| Label | Rows | Design section | Test ID | Evidence |
|---|---|---|---|---|
| FR-001 | `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R001` | [plan.md](plan.md) | T-001 | [test-spec.md](test-spec.md) |
| FR-002 | `CONN-FIREFLY-III-MCP-CONNECTOR-CONTENT-R002` | [plan.md](plan.md) | T-002 | [test-spec.md](test-spec.md) |
