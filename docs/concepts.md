# Concept Registry — firefly-iii-mcp

> **Prefix**: `CONCEPT:FF-*`
> **Version**: 0.1.0
> **Bridge**: [`CONCEPT:ECO-4.0`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:FF-001` | Firefly III API Domains | Action-routed + verbose 1:1 MCP tool surface over the Firefly III v1 REST API (28 domains, 230 operations): `about`, `accounts`, `attachments`, `autocomplete`, `available_budgets`, `bills`, `budgets`, `categories`, `charts`, `configuration`, `currencies`, `currency_exchange_rates`, `data`, `insight`, `links`, `object_groups`, `piggy_banks`, `preferences`, `recurrences`, `rule_groups`, `rules`, `search`, `summary`, `tags`, `transactions`, `user_groups`, `users`, `webhooks`. |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:ECO-4.0` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:ORCH-1.2` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:OS-5.1` | Prompt Injection Defense | agent-utilities |
