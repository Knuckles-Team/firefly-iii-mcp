---
name: firefly-iii-budgeting
skill_type: skill
description: >-
  Plan and track spending in Firefly III via the firefly-iii-mcp MCP server —
  manage budgets and per-period budget limits, categories, recurring bills, and
  piggy-bank savings goals, and read what has been spent against each. Use when the
  agent must create/inspect a budget envelope, set a monthly budget limit, categorize
  spending, track a recurring bill, or fund a savings goal. Do NOT use for account
  CRUD (use firefly-iii-account-management) or for booking individual transactions
  (use firefly-iii-transaction-ledger).
license: MIT
tags: [firefly-iii, budgets, categories, bills, savings, personal-finance, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Firefly III Budgeting

Domain-typed access to Firefly III **budgets & budget limits**, **categories**,
**bills**, and **piggy banks** — the planning and tracking side of the ledger.
Prefer these tools over raw HTTP; they return JSON:API resources
(`{"id":..,"attributes":{..}}`).

## When to use
- Create / list budgets and set per-period **budget limits** (envelope caps).
- Read what has been spent against a budget or category (`list_transaction_by_*`).
- Categorize spending (create/list categories).
- Track recurring **bills** (rent, subscriptions) and their matched transactions.
- Manage **piggy banks** (savings goals) attached to an asset account.

## When NOT to use
- Creating the accounts money flows between → `firefly-iii-account-management`.
- Booking/editing the actual transactions that consume a budget →
  `firefly-iii-transaction-ledger` (reference the `budget_id`/`category_id` there).
- Bulk-loading budgets into the knowledge graph → governed source sync (Related).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`firefly-iii-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `FIREFLY_III_URL` | ✅ | Base URL of the Firefly III instance |
| `FIREFLY_III_TOKEN` | ✅ | Personal Access Token (Bearer) |
| `FIREFLY_III_SSL_VERIFY` | optional | TLS verification toggle |


## Tools
One typed tool per operation, each taking the path argument `id`, a `data` body object and/or a `params` query object.

- Budgets and limits: `firefly_iii_delete_budget`, `firefly_iii_delete_budget_limit`, `firefly_iii_get_available_budget`, `firefly_iii_get_budget`, `firefly_iii_get_budget_limit`, `firefly_iii_list_available_budget_by_currency`, `firefly_iii_list_available_budgets`, `firefly_iii_list_budget`, `firefly_iii_list_budget_limit`, `firefly_iii_list_budget_limit_by_budget`, `firefly_iii_list_budget_limit_by_currency`, `firefly_iii_store_budget`, `firefly_iii_store_budget_limit`, `firefly_iii_update_budget`, `firefly_iii_update_budget_limit`.
- Bills: `firefly_iii_delete_bill`, `firefly_iii_get_bill`, `firefly_iii_list_bill`, `firefly_iii_list_bill_by_currency`, `firefly_iii_list_bill_by_object_group`, `firefly_iii_store_bill`, `firefly_iii_update_bill`.
- Categories: `firefly_iii_delete_category`, `firefly_iii_get_category`, `firefly_iii_list_category`, `firefly_iii_store_category`, `firefly_iii_update_category`.
- Tags: `firefly_iii_delete_tag`, `firefly_iii_get_tag`, `firefly_iii_list_tag`, `firefly_iii_store_tag`, `firefly_iii_update_tag`.
- Savings goals: `firefly_iii_delete_piggy_bank`, `firefly_iii_get_piggy_bank`, `firefly_iii_list_event_by_piggy_bank`, `firefly_iii_list_piggy_bank`, `firefly_iii_list_piggy_bank_by_account`, `firefly_iii_list_piggy_bank_by_object_group`, `firefly_iii_store_piggy_bank`, `firefly_iii_update_piggy_bank`.

### Key parameters
- `id` — required for `get_*`/`update_*`/`delete_*` and the `*_by_*` reads; budget
  limits also take `limit_id`.
- `data` — field→value body for the `store_*`/`update_*` actions.
- `params` — query dict (`start`, `end`, `page`, `limit`).

## Recipes (tool arguments)
Create a "Groceries" budget:
```json
{"data":{"name":"Groceries","active":true}}
```
Set a monthly limit on budget 3 (Feb 2026, $600):
```json
{"id":"3","data":{"start":"2026-02-01","end":"2026-02-29","amount":"600.00","currency_code":"USD"}}
```
See what was spent against budget 3 this month:
```json
{"id":"3","params":{"start":"2026-02-01","end":"2026-02-29"}}
```
Create a recurring bill (rent, monthly, $1200–1300):
```json
{"data":{"name":"Rent","amount_min":"1200.00","amount_max":"1300.00","date":"2026-01-01","repeat_freq":"monthly","currency_code":"USD"}}
```
Open a piggy bank toward a $5,000 vacation on account 14:
```json
{"data":{"name":"Vacation fund","account_id":"14","target_amount":"5000.00"}}
```

## Gotchas
- Money fields (`amount`, `amount_min`, `target_amount`) are **strings**.
- A **budget** is the envelope; the **budget limit** is the per-period cap — creating
  a budget alone does not cap spending, you must `store_budget_limit` with a
  `start`/`end` range.
- `list_transaction_without_budget` surfaces un-envelops spend — useful for triage.
- Piggy banks attach to a single **asset** `account_id`; the target is aspirational,
  Firefly does not move money automatically.
- Bills only *match* transactions by rule; `repeat_freq` is one of
  `weekly`/`monthly`/`quarterly`/`half-year`/`yearly`.

## Related
- **`firefly-iii-transaction-ledger`** — book the transactions that consume budgets
  and categories, and settle bills.
- **`firefly-iii-account-management`** — the asset accounts piggy banks attach to.
- Graph population goes through the governed source-sync path described in `firefly-iii-finance-operations`.
