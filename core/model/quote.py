#!usr/bin/env python3


from datetime import datetime

from ..wrapper.markit_wrapper import MarkitOnDemmand
from .asset import Asset


class Quote():
    """Represents a quote of a specific asset (stock, currency, etc.).

    Attributes:
        name (str): the asset name (may be the company name, currency, etc.).
        symbol (str): the ticker symbol used for trading the asset (and to serve as an unique identifier).
        exchange (str): the name of the exchange where the asset is traded.
        last_price (float): the last price (quote) of the asset.
        change_1h (float): The change in price of the asset since the last hour. Used for cryptomarkets only.
        change_percent_1h (float): The change percent in price of the asset since the last hour. Used for cryptomarkets only.
        change_1d (float): The change in price of the asset since last the day.
        change_percent_1d: The change percent in price of the asset since last the day.
        change_7d (float): The change in price of the asset since the last 07 days.
        change_percent_7d (float): The change percent in price of the asset since the last 07 days.
        change_year (float): The change in price of the asset since the beggining of the year.
        change_percent_year (float): The change percent in price of the asset since the beggining of the year.
        date_time (datetime): The last time the asset was traded in exchange-local timezone.
        market_cap (float): The asset's market cap.
        volume (float): The trade volume of the asset.
        high (float): The high price of the asset in the trading session.
        low (float): The low price of the asset in the trading session.
        open (float): The opening price of the asset at the start of the trading session.

    """

    def __init__(self,
                 name='',
                 symbol=''):
        """Class constructor. Initilizes attributes with specified or default values.

        Args:
            name (str): the name of the asset.
            symbol (str): the ticker symbol used for trading the asset (and to serve as an unique identifier).

        """

        self.name = name
        self.symbol = symbol
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
        self.date_time = datetime.now
        self.market_cap = 0
        self.volume = 0
        self.high = 0.0
        self.low = 0.0
        self.open = 0.0

    @staticmethod
    def from_market_data(ticker_symbol):
        """Creates a new instance with updated market data based on a specific 'ticker_symbol'.

        Args:
            ticker_symbol (str): The ticker symbol to look for updated market data.

        Returns:
            AssetQuote: a new instance with attributes updated with market values.

        """

        quote = Quote()
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
