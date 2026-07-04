# Concept Registry — firefly-iii-mcp

> **Prefix**: `CONCEPT:FF-*`
> **Version**: 0.1.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:FF-OS.config.ff` | Firefly III API Domains | Action-routed + verbose 1:1 MCP tool surface over the Firefly III v1 REST API (28 domains, 230 operations): `about`, `accounts`, `attachments`, `autocomplete`, `available_budgets`, `bills`, `budgets`, `categories`, `charts`, `configuration`, `currencies`, `currency_exchange_rates`, `data`, `insight`, `links`, `object_groups`, `piggy_banks`, `preferences`, `recurrences`, `rule_groups`, `rules`, `search`, `summary`, `tags`, `transactions`, `user_groups`, `users`, `webhooks`. |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
