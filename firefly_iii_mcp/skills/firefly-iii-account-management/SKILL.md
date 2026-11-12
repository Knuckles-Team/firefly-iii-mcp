---
name: firefly-iii-account-management
skill_type: skill
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
  author: Knuckles-Team
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
  governed source sync (see Related), not the CRUD surface below.

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`firefly-iii-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `FIREFLY_III_URL` | ✅ | Base URL of the Firefly III instance (the `/api` suffix is added automatically) |
| `FIREFLY_III_TOKEN` | ✅ | Personal Access Token (Bearer) |
| `FIREFLY_III_SSL_VERIFY` | optional | TLS verification toggle (default true) |

OIDC token-exchange delegation is used automatically when `ENABLE_DELEGATION` is
active; otherwise the fixed `FIREFLY_III_TOKEN` is used.

## Tools
One typed tool per operation, each taking the path argument `id` (or `code` for currencies), a `data` body object and/or a `params` query object.

- Accounts: `firefly_iii_delete_account`, `firefly_iii_get_account`, `firefly_iii_list_account`, `firefly_iii_list_account_by_currency`, `firefly_iii_store_account`, `firefly_iii_update_account`.
- Currencies and exchange rates: `firefly_iii_delete_currency`, `firefly_iii_delete_specific_currency_exchange_rate`, `firefly_iii_delete_specific_currency_exchange_rate_on_date`, `firefly_iii_delete_specific_currency_exchange_rates`, `firefly_iii_disable_currency`, `firefly_iii_enable_currency`, `firefly_iii_get_currency`, `firefly_iii_get_primary_currency`, `firefly_iii_list_currency`, `firefly_iii_list_currency_exchange_rates`, `firefly_iii_list_specific_currency_exchange_rate`, `firefly_iii_list_specific_currency_exchange_rate_on_date`, `firefly_iii_list_specific_currency_exchange_rates`, `firefly_iii_primary_currency`, `firefly_iii_store_currency`, `firefly_iii_store_currency_exchange_rate`, `firefly_iii_store_currency_exchange_rates_by_date`, `firefly_iii_store_currency_exchange_rates_by_pair`, `firefly_iii_update_currency`, `firefly_iii_update_currency_exchange_rate`, `firefly_iii_update_currency_exchange_rate_by_date`.

### Key parameters
- `id` — required for `get_account`, `update_account`, `delete_account`, and the
  `*_by_account` reads.
- `data` — object of field→value for `store_account` / `update_account`
  (`name`, `type`, `account_role`, `currency_code`, `opening_balance`, `iban`, …).
- `params` — query dict (`type`, `page`, `limit`, `start`, `end`).

## Recipes (tool arguments)
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
- Graph population goes through the governed source-sync path described in `firefly-iii-finance-operations`, not through account CRUD.
