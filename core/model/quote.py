#!usr/bin/env python3


from datetime import datetime

from ..wrapper.markit_wrapper import MarkitOnDemmand
from .asset import Asset


class Quote():
    """Represents a quote of a specific asset (stock, currency, etc.)."""

    def __init__(self):
        """Class constructor."""

        self.name = ''
        self.symbol = ''
        self.exchange = ''
        self.last_price = 0.0
        self.change_1h = 0.0  # Used for cryptomarkets only
        self.change_percent_1h = 0.0  # Used for cryptomarkets only
        self.change_1d = 0.0  # Used for stock and cryptomarkets
        self.change_percent_1d = 0.0  # Used for stock and cryptomarkets
        self.change_7d = 0.0  # Used for cryptomarkets only
        self.change_percent_7d = 0.0  # Used for cryptomarkets only
        self.change_year = 0.0  # Used for stock and cryptomarkets
        self.change_percent_year = 0.0  # Used for stock and cryptomarkets
        self.timestamp = datetime.now
        self.market_cap = 0
        self.volume = 0
        self.high = 0.0
        self.low = 0.0
        self.open = 0.0

    @classmethod
    def from_market_data(cls, ticker_symbol):
        """Creates a new instance with updated market data based on a specific 'ticker_symbol'.

        Args:
            ticker_symbol (str): The ticker symbol to look for updated market data.

        Returns:
            AssetQuote: a new instance with attributes updated with market values.

        """

        quote = cls()
        quote.__dict__.update(MarkitOnDemmand.quote(ticker_symbol))
        quote.exchange = Asset.get_exchange_name(quote.symbol)
        return quote

    def set_exchange_from_market_data(self):
        """Uses instance 'symbol' to search the market for the 'exchange' where the symbol is traded.

        If an exchange name is found, sets the instance's attribute 'exchange' with the name found.
        Otherwise, keeps the current value of instance 's ' exchange ' attribute.
        """

        name = Asset.get_exchange_name(self.symbol)
        if name is not None:
            self.exchange = name
