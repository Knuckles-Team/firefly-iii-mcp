from typing import Any

from .api_client_base import ApiClientBase


class ApiClientAutocomplete(ApiClientBase):
    """Firefly III `autocomplete` domain API operations."""

    def get_accounts_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all accounts of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/accounts", params=params)

    def get_bills_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all bills of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/bills", params=params)

    def get_budgets_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all budgets of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/budgets", params=params)

    def get_categories_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all categories of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/categories", params=params)

    def get_currencies_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all currencies of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/currencies", params=params)

    def get_currencies_code_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all currencies of the user returned in a basic auto-complete array. This endpoint is DEPRECATED and I suggest you DO NOT use it."""
        return self.request(
            "GET", "/v1/autocomplete/currencies-with-code", params=params
        )

    def get_object_groups_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all object groups of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/object-groups", params=params)

    def get_piggies_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all piggy banks of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/piggy-banks", params=params)

    def get_piggies_balance_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all piggy banks of the user returned in a basic auto-complete array."""
        return self.request(
            "GET", "/v1/autocomplete/piggy-banks-with-balance", params=params
        )

    def get_recurring_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all recurring transactions of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/recurring", params=params)

    def get_rule_groups_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all rule groups of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/rule-groups", params=params)

    def get_rules_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all rules of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/rules", params=params)

    def get_subscriptions_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all subscriptions of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/subscriptions", params=params)

    def get_tag_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all tags of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/tags", params=params)

    def get_transaction_types_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all transaction types returned in a basic auto-complete array. English only."""
        return self.request("GET", "/v1/autocomplete/transaction-types", params=params)

    def get_transactions_ac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all transaction descriptions of the user returned in a basic auto-complete array."""
        return self.request("GET", "/v1/autocomplete/transactions", params=params)

    def get_transactions_idac(self, params: dict | None = None) -> dict[str, Any]:
        """Returns all transactions, complemented with their ID, of the user returned in a basic auto-complete array. This endpoint is DEPRECATED and I suggest you DO NOT use it."""
        return self.request(
            "GET", "/v1/autocomplete/transactions-with-id", params=params
        )
