#!usr/bin/env python3


from datetime import datetime

from ..wrapper.markit_wrapper import MarkitOnDemmand


class Quote():
    """Represents a quote of a specific asset (stock, currency, etc.)."""

    def __init(self):
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

    def __str__(self):
        """Creates a custom string representation of this instance.

        Returns:
            str: a string representation of this instance.

        """

        return str(self.__dict__)

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
        quote.exchange = quote.get_exchange_name(quote.symbol)
        return quote

    @staticmethod
    def get_exchange_name(ticker_symbol):
        """Gets the exchange where 'ticker_symbol' is traded.

        Args:
            ticker_symbol (str): used to identify the exchange where the 'ticker_symbol' is traded.

        Returns:
            None: if no exchange was found based on 'ticker_symbol'. Otherwise;
            string: the name of the exchange where 'ticker_symbol' is traded.
                If 'ticker_symbol' is traded in more than one exchange,
                returns the first exchange found.

        Raises:
            ValueError: if an error message is returned from the API.

        """
        return MarkitOnDemmand.lookup_exchange(ticker_symbol)

    def get_ticker_symbol(self, company_name):
        return MarkitOnDemmand.lookup(company_name)
