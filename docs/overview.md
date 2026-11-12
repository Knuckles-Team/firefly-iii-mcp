# firefly-iii-mcp — Concept Overview

> **Category**: Integration | **Ecosystem Role**: MCP Server + A2A Agent
> Built on [`scion-sdk`](https://github.com/Knuckles-Team/scion-sdk) — the unified AGI Harness.

## Description

Firefly III API + MCP Server + A2A Agent — personal finance manager

## Architecture

This project follows the standardized agent-package pattern:

- **Modular Design**: the `api/` client mixins; the SDK derives one typed tool per
  client method.
- **Typed tools**: every tool is one Firefly III operation with typed arguments.
- **A2A Agent Server**: a Pydantic-AI graph agent (console script `firefly-iii-agent`)
  that calls the MCP tool surface and exposes an AG-UI web interface.
- **Verified Transport**: the client resolves a mandatory TLS profile from AgentConfig;
  the connector has no verification-disable control.
- **Governed Provider Bundle**: one complete skill, a neutral finance ontology,
  source presets, exact local schema fingerprints, SHACL shapes, fixtures, migrations,
  and a signed offline source attestation are owned by this distribution.

## Concept Registry

This project implements or inherits the following ecosystem concepts:

| Concept ID | Description | Source |
|:-----------|:------------|:-------|
| ECO-4.1 | MCP & Universal Skills | `scion-sdk` (inherited) |
| AU-ECO.toolkit.journey-map-narrative | A2A Network & Consensus | `scion-sdk` (inherited) |

> 📖 **Full Registry**: See [`scion-sdk/docs/overview.md`](https://github.com/Knuckles-Team/scion-sdk/blob/main/docs/overview.md) for the complete 5-Pillar concept index.
