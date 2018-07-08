#!usr/bin/env python3


from datetime import datetime

from core.wrapper.markit_wrapper import MarkitOnDemmand


class AssetQuote():
    """Represents a quote of a specific asset (stock, currency, etc.)."""

    def __init(self):
        self.name = ''
        self.symbol = ''
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

    def __str__(self):
        """Creates a custom string representation of this instance.

        Returns:
            str: a string representation of this instance.

        """

        return str(self.__dict__)

    @staticmethod
    def from_market_data(ticker_symbol):
        """Creates a new instance with updated market data based on a specific 'ticker_symbol'.

        Args:
            ticker_symbol (str): The ticker symbol to look for updated market data.

        Returns:
            AssetQuote: a new instance with attributes updated with market values.

        """

        quote = AssetQuote()
        quote.__dict__.update(MarkitOnDemmand.quote(ticker_symbol))
        return quote

    def get_ticker_symbol(self, company_name):
        return MarkitOnDemmand.lookup(company_name)
