# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- AgentConfig-backed mandatory TLS profiles and a portable configuration/privacy guide.
- One comprehensive Firefly III finance-operations provider skill with UI metadata.
- Connector-owned, instance-neutral accounts, transactions, and budgets source presets.

### Changed

- Migrated the full MCP surface to the current Agent Utilities modules and runtime extras.
- Externalized endpoints, credentials, model selection, trust, and telemetry destinations.

### Removed

- Direct finance-record graph writes and their internal transaction fallback; graph
  synchronization now requires the centrally compiled and approved capability path.
- The legacy API facade and three overlapping provider skills.

## [0.1.0] - 2026-06-22

### Added
- Initial release.
- Modular subfolders for API wrappers (`api/`) and action-routed MCP tools (`mcp/`).
- Material-theme mkdocs documentation site (7 standard pages).
- Full pre-commit quality gate and flat `tests/` structure.
