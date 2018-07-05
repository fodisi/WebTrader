#!usr/bin/env python3


from datetime import datetime

from core.wrapper.asset_wrapper import AssetWrapper


class Asset():

    def __init(self):
        self.name = ''
        self.symbol = ''
        self.exchange = ''
        self.last_price = 0.0
        self.change_1h = 0.0  # Used for cryptomarkets only
        self.change_percent_1h = 0.0  # Used for cryptomarkets only
        self.change_1d = 0.0  # Used for stock and cryptomarkets
        self.change_percent_1d = 0.0  # Used for stock cryptomarkets
        self.change_7d = 0.0  # Used for cryptomarkets only
        self.change_percent_7d = 0.0  # Used for cryptomarkets only
        self.timestamp = datetime.now
        self.market_cap = 0
        self.volume = 0
        self.change_ytd = 0.0
        self.change_ytd_percent = 0.0
        self.high = 0.0
        self.low = 0.0
        self.open = 0.0

    def get_last_price(self, ticker_symbol):
        return AssetWrapper().get_last_price(ticker_symbol)

    def get_ticker_symbol(self, company_name):
        return AssetWrapper().get_ticker_symbol(company_name)
