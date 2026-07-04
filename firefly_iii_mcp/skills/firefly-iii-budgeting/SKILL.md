---
name: firefly-iii-budgeting
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
  author: Genius
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
- Bulk-loading budgets into the knowledge graph → `firefly_ingest_budgets` (Related).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`firefly-iii-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `FIREFLY_III_URL` | ✅ | Base URL of the Firefly III instance |
| `FIREFLY_III_TOKEN` | ✅ | Personal Access Token (Bearer) |
| `FIREFLY_III_SSL_VERIFY` | optional | TLS verification toggle |

`MCP_TOOL_MODE` (`condensed`|`verbose`|`both`) selects the condensed surface (below)
vs. the 1:1 verbose tools.

## Tools & actions
Prefer the **condensed** tools; each takes `action` + a `params_json` **JSON string**.

| Condensed tool | Actions |
|----------------|---------|
| `budgets_operations` | `list_budget`, `get_budget`, `store_budget`, `update_budget`, `delete_budget`, `list_budget_limit`, `store_budget_limit`, `get_budget_limit`, `list_transaction_by_budget`, `list_transaction_without_budget` |
| `categories_operations` | `list_category`, `get_category`, `store_category`, `update_category`, `delete_category`, `list_transaction_by_category` |
| `bills_operations` | `list_bill`, `get_bill`, `store_bill`, `update_bill`, `delete_bill`, `list_transaction_by_bill` |
| `piggy_banks_operations` | `list_piggy_bank`, `get_piggy_bank`, `store_piggy_bank`, `update_piggy_bank`, `delete_piggy_bank`, `list_event_by_piggy_bank` |

### Key parameters
- `id` — required for `get_*`/`update_*`/`delete_*` and the `*_by_*` reads; budget
  limits also take `limit_id`.
- `data` — field→value body for the `store_*`/`update_*` actions.
- `params` — query dict (`start`, `end`, `page`, `limit`).

## Recipes (`params_json`)
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
- `params_json` is a **string** of JSON — serialize it.
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
- Native KG ingestion: `firefly_ingest_budgets` pushes budgets into the
  epistemic-graph as typed `:Budget` nodes.
