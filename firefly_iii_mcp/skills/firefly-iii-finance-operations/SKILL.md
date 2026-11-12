---
name: firefly-iii-finance-operations
skill_type: skill
description: Operate Firefly III through the firefly-iii-mcp typed tools, covering accounts, currencies, transactions and splits, budgets and limits, categories, bills, savings goals, rules, recurrences, reports, attachments, users, webhooks, and governed source synchronization. Use when an agent must inspect or safely change a Firefly III ledger, reconcile or report on finance records, configure automation, or prepare approved Firefly III data for Arbora ingestion.
---

# Firefly III finance operations

Every tool is one Firefly III operation with typed arguments: the path argument `id` (or `code`), a `data` body object, and/or a `params` query object.

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

| Need | Tools |
| --- | --- |
| Service metadata and configuration | `firefly_iii_get_about`, `firefly_iii_get_configuration`, `firefly_iii_get_cron`, `firefly_iii_get_preference`, `firefly_iii_get_single_configuration`, `firefly_iii_list_preference`, `firefly_iii_set_configuration`, `firefly_iii_store_preference`, `firefly_iii_update_preference` |
| Accounts and denomination | `firefly_iii_delete_account`, `firefly_iii_get_account`, `firefly_iii_list_account`, `firefly_iii_list_account_by_currency`, `firefly_iii_store_account`, `firefly_iii_update_account`, `firefly_iii_delete_currency`, `firefly_iii_delete_specific_currency_exchange_rate`, `firefly_iii_delete_specific_currency_exchange_rate_on_date`, `firefly_iii_delete_specific_currency_exchange_rates`, `firefly_iii_disable_currency`, `firefly_iii_enable_currency`, `firefly_iii_get_currency`, `firefly_iii_get_primary_currency`, `firefly_iii_list_currency`, `firefly_iii_list_currency_exchange_rates`, `firefly_iii_list_specific_currency_exchange_rate`, `firefly_iii_list_specific_currency_exchange_rate_on_date`, `firefly_iii_list_specific_currency_exchange_rates`, `firefly_iii_primary_currency`, `firefly_iii_store_currency`, `firefly_iii_store_currency_exchange_rate`, `firefly_iii_store_currency_exchange_rates_by_date`, `firefly_iii_store_currency_exchange_rates_by_pair`, `firefly_iii_update_currency`, `firefly_iii_update_currency_exchange_rate`, `firefly_iii_update_currency_exchange_rate_by_date` |
| Ledger entries and relationships | `firefly_iii_bulk_update_transactions`, `firefly_iii_delete_link_type`, `firefly_iii_delete_transaction`, `firefly_iii_delete_transaction_journal`, `firefly_iii_delete_transaction_link`, `firefly_iii_finish_batch`, `firefly_iii_get_link_type`, `firefly_iii_get_transaction`, `firefly_iii_get_transaction_by_journal`, `firefly_iii_get_transaction_link`, `firefly_iii_list_event_by_transaction`, `firefly_iii_list_link_type`, `firefly_iii_list_links_by_journal`, `firefly_iii_list_transaction`, `firefly_iii_list_transaction_by_account`, `firefly_iii_list_transaction_by_bill`, `firefly_iii_list_transaction_by_budget`, `firefly_iii_list_transaction_by_budget_limit`, `firefly_iii_list_transaction_by_category`, `firefly_iii_list_transaction_by_currency`, `firefly_iii_list_transaction_by_link_type`, `firefly_iii_list_transaction_by_tag`, `firefly_iii_list_transaction_link`, `firefly_iii_list_transaction_without_budget`, `firefly_iii_store_link_type`, `firefly_iii_store_transaction`, `firefly_iii_store_transaction_link`, `firefly_iii_update_link_type`, `firefly_iii_update_transaction`, `firefly_iii_update_transaction_link`, `firefly_iii_delete_tag`, `firefly_iii_get_tag`, `firefly_iii_list_tag`, `firefly_iii_store_tag`, `firefly_iii_update_tag`, `firefly_iii_delete_attachment`, `firefly_iii_download_attachment`, `firefly_iii_get_attachment`, `firefly_iii_list_attachment`, `firefly_iii_list_attachment_by_account`, `firefly_iii_list_attachment_by_bill`, `firefly_iii_list_attachment_by_budget`, `firefly_iii_list_attachment_by_category`, `firefly_iii_list_attachment_by_piggy_bank`, `firefly_iii_list_attachment_by_tag`, `firefly_iii_list_attachment_by_transaction`, `firefly_iii_store_attachment`, `firefly_iii_update_attachment`, `firefly_iii_upload_attachment` |
| Planning and savings | `firefly_iii_delete_budget`, `firefly_iii_delete_budget_limit`, `firefly_iii_get_available_budget`, `firefly_iii_get_budget`, `firefly_iii_get_budget_limit`, `firefly_iii_list_available_budget_by_currency`, `firefly_iii_list_available_budgets`, `firefly_iii_list_budget`, `firefly_iii_list_budget_limit`, `firefly_iii_list_budget_limit_by_budget`, `firefly_iii_list_budget_limit_by_currency`, `firefly_iii_store_budget`, `firefly_iii_store_budget_limit`, `firefly_iii_update_budget`, `firefly_iii_update_budget_limit`, `firefly_iii_delete_category`, `firefly_iii_get_category`, `firefly_iii_list_category`, `firefly_iii_store_category`, `firefly_iii_update_category`, `firefly_iii_delete_bill`, `firefly_iii_get_bill`, `firefly_iii_list_bill`, `firefly_iii_list_bill_by_currency`, `firefly_iii_list_bill_by_object_group`, `firefly_iii_store_bill`, `firefly_iii_update_bill`, `firefly_iii_delete_piggy_bank`, `firefly_iii_get_piggy_bank`, `firefly_iii_list_event_by_piggy_bank`, `firefly_iii_list_piggy_bank`, `firefly_iii_list_piggy_bank_by_account`, `firefly_iii_list_piggy_bank_by_object_group`, `firefly_iii_store_piggy_bank`, `firefly_iii_update_piggy_bank` |
| Automation | `firefly_iii_delete_rule`, `firefly_iii_delete_rule_group`, `firefly_iii_fire_rule`, `firefly_iii_fire_rule_group`, `firefly_iii_get_rule`, `firefly_iii_get_rule_group`, `firefly_iii_list_rule`, `firefly_iii_list_rule_by_bill`, `firefly_iii_list_rule_by_currency`, `firefly_iii_list_rule_by_group`, `firefly_iii_list_rule_group`, `firefly_iii_store_rule`, `firefly_iii_store_rule_group`, `firefly_iii_test_rule`, `firefly_iii_test_rule_group`, `firefly_iii_update_rule`, `firefly_iii_update_rule_group`, `firefly_iii_delete_recurrence`, `firefly_iii_get_recurrence`, `firefly_iii_list_recurrence`, `firefly_iii_list_recurrence_by_currency`, `firefly_iii_list_transaction_by_recurrence`, `firefly_iii_store_recurrence`, `firefly_iii_trigger_recurrence_recurrence`, `firefly_iii_update_recurrence`, `firefly_iii_delete_webhook`, `firefly_iii_delete_webhook_message`, `firefly_iii_delete_webhook_message_attempt`, `firefly_iii_get_single_webhook_message`, `firefly_iii_get_single_webhook_message_attempt`, `firefly_iii_get_webhook`, `firefly_iii_get_webhook_message_attempts`, `firefly_iii_get_webhook_messages`, `firefly_iii_list_webhook`, `firefly_iii_store_webhook`, `firefly_iii_submit_webhook`, `firefly_iii_trigger_transaction_webhook`, `firefly_iii_update_webhook` |
| Discovery and reporting | `firefly_iii_get_accounts_ac`, `firefly_iii_get_bills_ac`, `firefly_iii_get_budgets_ac`, `firefly_iii_get_categories_ac`, `firefly_iii_get_currencies_ac`, `firefly_iii_get_currencies_code_ac`, `firefly_iii_get_object_groups_ac`, `firefly_iii_get_piggies_ac`, `firefly_iii_get_piggies_balance_ac`, `firefly_iii_get_recurring_ac`, `firefly_iii_get_rule_groups_ac`, `firefly_iii_get_rules_ac`, `firefly_iii_get_subscriptions_ac`, `firefly_iii_get_tag_ac`, `firefly_iii_get_transaction_types_ac`, `firefly_iii_get_transactions_ac`, `firefly_iii_get_transactions_idac`, `firefly_iii_search_accounts`, `firefly_iii_search_transactions`, `firefly_iii_get_basic_summary`, `firefly_iii_get_chart_account_overview`, `firefly_iii_get_chart_balance`, `firefly_iii_get_chart_budget_overview`, `firefly_iii_get_chart_category_overview`, `firefly_iii_insight_expense_asset`, `firefly_iii_insight_expense_bill`, `firefly_iii_insight_expense_budget`, `firefly_iii_insight_expense_category`, `firefly_iii_insight_expense_expense`, `firefly_iii_insight_expense_no_bill`, `firefly_iii_insight_expense_no_budget`, `firefly_iii_insight_expense_no_category`, `firefly_iii_insight_expense_no_tag`, `firefly_iii_insight_expense_tag`, `firefly_iii_insight_expense_total`, `firefly_iii_insight_income_asset`, `firefly_iii_insight_income_category`, `firefly_iii_insight_income_no_category`, `firefly_iii_insight_income_no_tag`, `firefly_iii_insight_income_revenue`, `firefly_iii_insight_income_tag`, `firefly_iii_insight_income_total`, `firefly_iii_insight_transfer_category`, `firefly_iii_insight_transfer_no_category`, `firefly_iii_insight_transfer_no_tag`, `firefly_iii_insight_transfer_tag`, `firefly_iii_insight_transfer_total`, `firefly_iii_insight_transfers` |
| Administration and data lifecycle | `firefly_iii_delete_object_group`, `firefly_iii_delete_user`, `firefly_iii_get_current_user`, `firefly_iii_get_object_group`, `firefly_iii_get_user`, `firefly_iii_get_user_group`, `firefly_iii_list_object_groups`, `firefly_iii_list_user`, `firefly_iii_list_user_groups`, `firefly_iii_store_user`, `firefly_iii_update_object_group`, `firefly_iii_update_user`, `firefly_iii_update_user_group`, `firefly_iii_destroy_data`, `firefly_iii_export_accounts`, `firefly_iii_export_bills`, `firefly_iii_export_budgets`, `firefly_iii_export_categories`, `firefly_iii_export_piggies`, `firefly_iii_export_recurring`, `firefly_iii_export_rules`, `firefly_iii_export_tags`, `firefly_iii_export_transactions`, `firefly_iii_purge_data` |

Read the tool's current argument schema before calling it. Do not infer a field from an older Firefly III release.

## Execute safely

1. Read the exact records and stable identifiers needed for the task.
2. Validate the requested operation against those records. For transactions, confirm
   direction, source and destination accounts, currency, amount, date, and every split.
3. Present the intended mutation before executing any create, update, delete, import,
   purge, rule, recurrence, webhook, or administrative action. Obtain explicit approval
   when the request did not already provide it.
4. Execute the narrowest tool. Keep arguments bounded and omit unrelated fields.
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

List records with query parameters: call `firefly_iii_list_account` with `params` = `{"type":"asset"}`.

Read one record: call `firefly_iii_get_account` with `id` = `<account-id>`.

Create a transaction only after the execution-safety checks: call `firefly_iii_store_transaction` with `data` = `{"transactions":[{"type":"transfer","date":"<iso-date>","amount":"<decimal>","description":"<description>","source_id":"<source-id>","destination_id":"<destination-id>"}]}`.

## Use governed graph synchronization

Do not write Firefly III records directly into epistemic-graph. This provider supplies
neutral source presets and an ontology as human-reviewed compiler inputs; it does not
ship live tool-schema fingerprints or a signed capability bundle. Use the Arbora
source-sync path only after the central compiler has generated the current schema-v2
bundle and an operator has approved its tenant, ACL, classification, retention,
provenance, redaction, and deletion policy. Missing governance must fail closed.

When synchronization is approved, invoke the central `source_sync`/Arbora capability
with the provider preset; do not call a connector-local graph-write tool or create an
alternate ingestion path.
