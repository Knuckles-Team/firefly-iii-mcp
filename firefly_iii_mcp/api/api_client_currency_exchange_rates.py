from typing import Any

from .api_client_base import ApiClientBase


class ApiClientCurrencyExchangeRates(ApiClientBase):
    """Firefly III `currency_exchange_rates` domain API operations."""

    def list_currency_exchange_rates(
        self, params: dict | None = None
    ) -> dict[str, Any]:
        """List all exchange rates that Firefly III knows."""
        return self.request("GET", "/v1/exchange-rates", params=params)

    def store_currency_exchange_rate(
        self, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store a new currency exchange rate."""
        return self.request("POST", "/v1/exchange-rates", json=data, params=params)

    def list_specific_currency_exchange_rate(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List a single specific exchange rate."""
        return self.request("GET", f"/v1/exchange-rates/{id}", params=params)

    def delete_specific_currency_exchange_rate(
        self, id: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Delete a specific currency exchange rate."""
        return self.request("DELETE", f"/v1/exchange-rates/{id}", params=params)

    def update_currency_exchange_rate(
        self, id: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Update existing currency exchange rate."""
        return self.request("PUT", f"/v1/exchange-rates/{id}", json=data, params=params)

    def list_specific_currency_exchange_rates(
        self, from_: str, to: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List all exchange rates from/to the mentioned currencies."""
        return self.request("GET", f"/v1/exchange-rates/{from_}/{to}", params=params)

    def delete_specific_currency_exchange_rates(
        self, from_: str, to: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Deletes ALL currency exchange rates from 'from' to 'to'."""
        return self.request("DELETE", f"/v1/exchange-rates/{from_}/{to}", params=params)

    def list_specific_currency_exchange_rate_on_date(
        self, from_: str, to: str, date: str, params: dict | None = None
    ) -> dict[str, Any]:
        """List the exchange rate for the from and to-currency on the requested date."""
        return self.request(
            "GET", f"/v1/exchange-rates/{from_}/{to}/{date}", params=params
        )

    def delete_specific_currency_exchange_rate_on_date(
        self, from_: str, to: str, date: str, params: dict | None = None
    ) -> dict[str, Any]:
        """Delete the currency exchange rate from 'from' to 'to' on the specified date."""
        return self.request(
            "DELETE", f"/v1/exchange-rates/{from_}/{to}/{date}", params=params
        )

    def update_currency_exchange_rate_by_date(
        self,
        from_: str,
        to: str,
        date: str,
        data: dict | None = None,
        params: dict | None = None,
    ) -> dict[str, Any]:
        """Update existing currency exchange rate."""
        return self.request(
            "PUT", f"/v1/exchange-rates/{from_}/{to}/{date}", json=data, params=params
        )

    def store_currency_exchange_rates_by_date(
        self, date: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store new currency exchange rates under this date"""
        return self.request(
            "POST", f"/v1/exchange-rates/by-date/{date}", json=data, params=params
        )

    def store_currency_exchange_rates_by_pair(
        self, from_: str, to: str, data: dict | None = None, params: dict | None = None
    ) -> dict[str, Any]:
        """Store new currency exchange rates under this from/to pair."""
        return self.request(
            "POST",
            f"/v1/exchange-rates/by-currencies/{from_}/{to}",
            json=data,
            params=params,
        )
