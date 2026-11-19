---
name: firefly-iii-transaction-ledger
skill_type: skill
description: >-
  Book and manage Firefly III transactions (withdrawals, deposits, transfers) via
  the firefly-iii-mcp MCP server — list, read, create, update, and delete
  double-entry transactions and their splits. Use when the agent must record a new
  expense/income/transfer, look up a transaction by id, edit or split an existing
  transaction, or reconcile the ledger. Do NOT use for creating accounts (use
  firefly-iii-account-management) or for budgets, bills and categories setup (use
  firefly-iii-budgeting).
license: MIT
tags: [firefly-iii, transactions, ledger, double-entry, rest-api, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Firefly III Transaction Ledger

Domain-typed access to Firefly III **transactions** — the double-entry ledger.
Every transaction is a *group* of one or more *splits* (journals), each moving money
from a `source_id` account to a `destination_id` account. Prefer these tools over raw
HTTP — they carry the split conventions and return JSON:API transaction resources.

## When to use
- Record a new **withdrawal** (expense), **deposit** (income), or **transfer**.
- List / filter transactions by date range or type.
- Fetch a single transaction (group) by `id`, or one split by journal id.
- Update or delete a transaction, or delete a single split from a group.

## When NOT to use
- Creating or editing the accounts money flows between →
  `firefly-iii-account-management`.
- Setting up budgets, budget limits, bills or categories → `firefly-iii-budgeting`
  (you still *reference* a `budget_id`/`category_id` on a split here).
- Bulk-loading history into the knowledge graph → the native
  governed source sync (see Related).

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`firefly-iii-mcp`** MCP server.

| Variable | Required | Notes |
|----------|----------|-------|
| `FIREFLY_III_URL` | ✅ | Base URL of the Firefly III instance |
| `FIREFLY_III_TOKEN` | ✅ | Personal Access Token (Bearer) |
| `FIREFLY_III_SSL_VERIFY` | optional | TLS verification toggle |


## Tools
One typed tool per operation, each taking the path argument `id`, a `data` body object and/or a `params` query object.

- Transactions, splits and links: `firefly_iii_bulk_update_transactions`, `firefly_iii_delete_link_type`, `firefly_iii_delete_transaction`, `firefly_iii_delete_transaction_journal`, `firefly_iii_delete_transaction_link`, `firefly_iii_finish_batch`, `firefly_iii_get_link_type`, `firefly_iii_get_transaction`, `firefly_iii_get_transaction_by_journal`, `firefly_iii_get_transaction_link`, `firefly_iii_list_event_by_transaction`, `firefly_iii_list_link_type`, `firefly_iii_list_links_by_journal`, `firefly_iii_list_transaction`, `firefly_iii_list_transaction_by_account`, `firefly_iii_list_transaction_by_bill`, `firefly_iii_list_transaction_by_budget`, `firefly_iii_list_transaction_by_budget_limit`, `firefly_iii_list_transaction_by_category`, `firefly_iii_list_transaction_by_currency`, `firefly_iii_list_transaction_by_link_type`, `firefly_iii_list_transaction_by_tag`, `firefly_iii_list_transaction_link`, `firefly_iii_list_transaction_without_budget`, `firefly_iii_store_link_type`, `firefly_iii_store_transaction`, `firefly_iii_store_transaction_link`, `firefly_iii_update_link_type`, `firefly_iii_update_transaction`, `firefly_iii_update_transaction_link`.
- Attachments: `firefly_iii_delete_attachment`, `firefly_iii_download_attachment`, `firefly_iii_get_attachment`, `firefly_iii_list_attachment`, `firefly_iii_list_attachment_by_account`, `firefly_iii_list_attachment_by_bill`, `firefly_iii_list_attachment_by_budget`, `firefly_iii_list_attachment_by_category`, `firefly_iii_list_attachment_by_piggy_bank`, `firefly_iii_list_attachment_by_tag`, `firefly_iii_list_attachment_by_transaction`, `firefly_iii_store_attachment`, `firefly_iii_update_attachment`, `firefly_iii_upload_attachment`.
- Recurring transactions: `firefly_iii_delete_recurrence`, `firefly_iii_get_recurrence`, `firefly_iii_list_recurrence`, `firefly_iii_list_recurrence_by_currency`, `firefly_iii_list_transaction_by_recurrence`, `firefly_iii_store_recurrence`, `firefly_iii_trigger_recurrence_recurrence`, `firefly_iii_update_recurrence`.

### Key parameters
- `id` — required for `get_transaction`, `update_transaction`, `delete_transaction`.
- `data` — the transaction body: `{"transactions":[ {split}, … ]}`. Each split
  carries `type` (`withdrawal`/`deposit`/`transfer`), `amount`, `description`,
  `date`, `source_id`, `destination_id`, and optional `category_id`, `budget_id`,
  `currency_code`, `tags`.
- `params` — query dict (`start`, `end`, `type`, `page`, `limit`).

## Recipes (tool arguments)
List this quarter's transactions:
```json
{"params":{"start":"2026-01-01","end":"2026-03-31","type":"withdrawal"}}
```
Record a $42.50 grocery withdrawal from account 12 to expense account 30:
```json
{"data":{"transactions":[{"type":"withdrawal","date":"2026-02-14","amount":"42.50","description":"Groceries","source_id":"12","destination_id":"30","category_id":"5","budget_id":"3","currency_code":"USD"}]}}
```
Record a transfer between two asset accounts:
```json
{"data":{"transactions":[{"type":"transfer","date":"2026-02-15","amount":"500.00","description":"Move to savings","source_id":"12","destination_id":"14"}]}}
```
Get one transaction group by id:
```json
{"id":"789"}
```

## Gotchas
- A transaction is a **group of splits**: the top-level body must wrap the splits in
  `{"transactions":[…]}`, even for a single split.
- `amount` and money fields are **strings**; `type` must match the account pair
  (`withdrawal` = asset→expense, `deposit` = revenue→asset, `transfer` = asset→asset).
- For `withdrawal`/`deposit` you can pass account **names** (`source_name`/
  `destination_name`) to auto-create expense/revenue accounts, but for `transfer`
  both `source_id` and `destination_id` must be existing asset accounts.
- `delete_transaction_journal` removes a single split; `delete_transaction` removes
  the whole group.

## Related
- **`firefly-iii-account-management`** — the accounts each split references.
- **`firefly-iii-budgeting`** — the budgets/categories a split books against.
- Graph population goes through the governed source-sync path described in `firefly-iii-finance-operations`.
