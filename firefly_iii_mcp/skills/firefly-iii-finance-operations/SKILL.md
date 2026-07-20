---
name: firefly-iii-finance-operations
skill_type: skill
description: Operate Firefly III through the firefly-iii-mcp action-routed tools, covering accounts, currencies, transactions and splits, budgets and limits, categories, bills, savings goals, rules, recurrences, reports, attachments, users, webhooks, and governed source synchronization. Use when an agent must inspect or safely change a Firefly III ledger, reconcile or report on finance records, configure automation, or prepare approved Firefly III data for GraphOS ingestion.
---

# Firefly III finance operations

Use the condensed tools unless the caller explicitly needs the verbose 1:1 surface.
Every condensed tool accepts an `action` plus `params_json`, where `params_json` is a
serialized JSON string containing path arguments, a `data` body, and/or query
`params`.

## Establish the boundary

- Connect only to the runtime-selected `firefly-iii-mcp` server.
- Require `FIREFLY_III_URL` to resolve to an HTTPS endpoint. Supply fixed credentials
  through `FIREFLY_III_TOKEN` only when OIDC delegation is disabled.
- Select private trust through the AgentConfig TLS profile catalog. Never add a
  verification toggle, certificate path, endpoint, or credential to source or skill
  content.
- Treat account names, balances, identifiers, transaction descriptions, amounts,
  dates, attachments, and user data as sensitive. Return only what the task needs and
  never copy tool payloads into logs, traces, prompts, or durable graph metadata.

## Choose the tool domain

| Need | Condensed tools |
| --- | --- |
| Service metadata and configuration | `about_operations`, `configuration_operations`, `preferences_operations` |
| Accounts and denomination | `accounts_operations`, `currencies_operations`, `currency_exchange_rates_operations` |
| Ledger entries and relationships | `transactions_operations`, `links_operations`, `tags_operations`, `attachments_operations` |
| Planning and savings | `budgets_operations`, `available_budgets_operations`, `categories_operations`, `bills_operations`, `piggy_banks_operations` |
| Automation | `rules_operations`, `rule_groups_operations`, `recurrences_operations`, `webhooks_operations` |
| Discovery and reporting | `search_operations`, `summary_operations`, `insight_operations`, `charts_operations`, `autocomplete_operations` |
| Administration and data lifecycle | `users_operations`, `user_groups_operations`, `object_groups_operations`, `data_operations` |

Discover the selected tool's current action schema before calling it. Do not infer an
action or field from an older Firefly III release.

## Execute safely

1. Read the exact records and stable identifiers needed for the task.
2. Validate the requested operation against those records. For transactions, confirm
   direction, source and destination accounts, currency, amount, date, and every split.
3. Present the intended mutation before executing any create, update, delete, import,
   purge, rule, recurrence, webhook, or administrative action. Obtain explicit approval
   when the request did not already provide it.
4. Execute the narrowest action. Keep `params_json` bounded and omit unrelated fields.
5. Read the affected object again and report the result without echoing sensitive
   fields unnecessarily.

Never use delete-and-recreate as an update strategy. Never invent balances, account
identifiers, exchange rates, totals, or reconciliation state.

## Apply Firefly III conventions

- Treat money values as decimal strings; do not convert them through binary floating
  point.
- Treat a transaction as a group containing one or more splits. Wrap create/update
  payloads in `{"transactions":[...]}`.
- Match transaction direction to the account pair: withdrawal moves asset to expense,
  deposit moves revenue to asset, and transfer moves asset to asset.
- Resolve concrete account IDs before booking. Do not rely on ambiguous display names.
- Distinguish a budget from its dated budget limit. Creating a budget does not set a
  spending ceiling.
- Read dependent transactions before deleting an account, category, budget, bill, or
  transaction group.
- Treat rules, recurrences, webhooks, imports, and data lifecycle actions as high-impact
  automation. Inspect current state and require a reviewable intent before mutation.

## Shape calls

List records with query parameters:

```json
{"action":"list_account","params_json":"{\"params\":{\"type\":\"asset\"}}"}
```

Read one record:

```json
{"action":"get_account","params_json":"{\"id\":\"<account-id>\"}"}
```

Create a transaction only after the execution-safety checks:

```json
{
  "action": "store_transaction",
  "params_json": "{\"data\":{\"transactions\":[{\"type\":\"transfer\",\"date\":\"<iso-date>\",\"amount\":\"<decimal>\",\"description\":\"<description>\",\"source_id\":\"<source-id>\",\"destination_id\":\"<destination-id>\"}]}}"
}
```

## Use governed graph synchronization

Do not write Firefly III records directly into epistemic-graph. This provider supplies
neutral source presets and an ontology as human-reviewed compiler inputs; it does not
ship live tool-schema fingerprints or a signed capability bundle. Use the GraphOS
source-sync path only after the central compiler has generated the current schema-v2
bundle and an operator has approved its tenant, ACL, classification, retention,
provenance, redaction, and deletion policy. Missing governance must fail closed.

When synchronization is approved, invoke the central `source_sync`/GraphOS capability
with the provider preset; do not call a connector-local graph-write tool or create an
alternate ingestion path.
