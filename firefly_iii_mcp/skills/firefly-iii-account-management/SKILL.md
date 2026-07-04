---
name: firefly-iii-account-management
description: >-
  Manage Firefly III accounts (asset, expense, revenue, liability, cash) and their
  currencies via the firefly-iii-mcp MCP server — list, read, create, and update
  accounts and inspect their balances and transactions. Use when the agent must
  enumerate the user's accounts, look up one account by id, open a new asset or
  liability account, or read an account's balance and recent transactions. Do NOT
  use for booking/editing individual transactions (use
  firefly-iii-transaction-ledger) or for budgets, bills and savings goals (use
  firefly-iii-budgeting).
license: MIT
tags: [firefly-iii, accounts, currencies, personal-finance, rest-api, mcp]
metadata:
  author: Genius
  version: '0.1.0'
---
# Firefly III Account Management

Domain-typed access to Firefly III **accounts** and **currencies** for personal
finance. Prefer these tools over raw HTTP — they carry the account field conventions
and return JSON:API account resources (`{"id":..,"attributes":{..}}`).

## When to use
- List / filter accounts (e.g. only asset accounts, or active accounts).
- Fetch a single account by `id`, including its `current_balance`.
- Create a new account (asset, expense, revenue, liability).
- Read an account's transactions or attachments.

## When NOT to use
- Booking, splitting, editing or deleting transactions → `firefly-iii-transaction-ledger`.
- Budgets, budget limits, bills, categories, piggy banks →
  `firefly-iii-budgeting`.
- Pushing accounts into the knowledge graph as typed nodes → the native
  `firefly_ingest_accounts` tool (see Related), not the CRUD surface below.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`firefly-iii-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `FIREFLY_III_URL` | ✅ | Base URL of the Firefly III instance (the `/api` suffix is added automatically) |
| `FIREFLY_III_TOKEN` | ✅ | Personal Access Token (Bearer) |
| `FIREFLY_III_SSL_VERIFY` | optional | TLS verification toggle (default true) |

OIDC token-exchange delegation is used automatically when `ENABLE_DELEGATION` is
active; otherwise the fixed `FIREFLY_III_TOKEN` is used. `MCP_TOOL_MODE`
(`condensed`|`verbose`|`both`) selects the condensed surface (used below) vs. the
1:1 verbose tools.

## Tools & actions
Prefer the **condensed** tool; it takes `action` + a `params_json` **JSON string**
whose keys are passed straight to the client method (path params, a `data` body dict,
and a `params` query dict).

| Condensed tool | Actions |
|----------------|---------|
| `accounts_operations` | `list_account`, `get_account`, `store_account`, `update_account`, `delete_account`, `list_transaction_by_account`, `list_attachment_by_account`, `list_piggy_bank_by_account` |
| `currencies_operations` | `list_currency`, `get_currency`, `store_currency`, … |

### Key parameters
- `id` — required for `get_account`, `update_account`, `delete_account`, and the
  `*_by_account` reads.
- `data` — object of field→value for `store_account` / `update_account`
  (`name`, `type`, `account_role`, `currency_code`, `opening_balance`, `iban`, …).
- `params` — query dict (`type`, `page`, `limit`, `start`, `end`).

## Recipes (`params_json`)
List active asset accounts:
```json
{"params":{"type":"asset"}}
```
Get one account by id:
```json
{"id":"12"}
```
Create a new asset (checking) account:
```json
{"data":{"name":"Everyday Checking","type":"asset","account_role":"defaultAsset","currency_code":"USD","opening_balance":"1500.00","opening_balance_date":"2026-01-01"}}
```
Read an account's recent transactions:
```json
{"id":"12","params":{"start":"2026-01-01","end":"2026-03-31"}}
```

## Gotchas
- `params_json` is a **string** of JSON, not an object — serialize it.
- Firefly returns **JSON:API** — the real fields live under `attributes`, and money
  values (`current_balance`, `opening_balance`) are **strings**, not numbers.
- `type` must be a valid Firefly account type (`asset`, `expense`, `revenue`,
  `liability`, `cash`); an asset account also needs an `account_role`.
- `currency_code` is an ISO code (e.g. `USD`), not a numeric currency id.
- Deleting an account with transactions moves those transactions too — read
  `list_transaction_by_account` first.

## Related
- **`firefly-iii-transaction-ledger`** — book and manage the transactions that hit
  these accounts.
- **`firefly-iii-budgeting`** — envelopes, bills and savings goals.
- Native KG ingestion: the `firefly_ingest_accounts` tool pushes accounts into the
  epistemic-graph as typed `:Account` nodes (with `:Currency` + `:denominatedIn`
  links). Use it for graph population, not day-to-day account CRUD.
