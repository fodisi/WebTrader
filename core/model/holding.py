#!/usr/bin/env python3

from ..mapper.holding_mapper import HoldingMapper
from .quote import Quote


class Holding:
    """A Holding summarizes all the buy and sell orders for a specific asset related to an account (user).
    Everytime an account buys a new asset, the volume bought is added to the specific asset holding record,
    and the average price of the asset is recalculated to reflect the last order.
    A similar process is performed when an account (user) sells an asset, decresing the holding volume of
    that specific asset.

    Attributes:
        id (int): a unique identifier for the holding record.
        username (str): the account's username that owns the asset.
        ticker_symbol (str): the asset owned.
        volume (float): the total volume owned by the account of a specific asset.
        average_price (float): average price paid for the asset, including fees.

    """

    BROKERAGE_FEE = 6.95
    """Default brokerage fee paid by each transaction. This is fixed for simplified use case."""

    def __init__(self,
                 id=0,
                 username='',
                 ticker_symbol='',
                 volume=0.0,
                 average_price=0.0):
        """Class constructor. Initializes attributes with specified or default values.

        Args:
            id (int): a unique identifier for the holding record.
            username (str): the account's username that owns the asset.
            ticker_symbol (str): the asset owned.
            volume (float): the total volume owned by the account of a specific asset.
            average_price (float): average price paid for the asset, including fees.

        """

        self.id = id
        self.username = username
        self.ticker_symbol = ticker_symbol
        self.volume = volume
        self.average_price = average_price

    def __dict_to_holding(self, obj):

        if not isinstance(obj, dict):
            msg = 'Invalid argument type. Expecting "{0}" type; Received "{1}" type.'
            raise TypeError(msg.format(dict, type(obj)))

        holding = Holding()
        holding.__dict__.update(obj)
        return holding

    def update_holdings(self, username, ticker_symbol, trade_volume,
                        trade_unit_price, transaction_type):
        # TODO REPLACE MAPPER FUNCTION BY CLASS FUNCTION
        # holdings = self.get_user_holdings_by_symbol(username, ticker_symbol)
        holdings = HoldingMapper().select_holdings_by_symbol(username, ticker_symbol)

        if holdings is not None:
            # Buy
            if transaction_type == 'B':
                # finds the new weighted average unit price and new volume
                total_weighted_price = holdings['volume'] * \
                    holdings['average_price']
                total_weighted_price += trade_volume * trade_unit_price
                total_volume = holdings['volume'] + trade_volume
                weighted_avg_price = total_weighted_price / float(total_volume)
                HoldingMapper().update_holdings(username,
                                                ticker_symbol,
                                                total_volume,
                                                weighted_avg_price)
            # Sell
            elif transaction_type == 'S':
                # when selling, the average price of holdings doesn't change,
                # except when remaining volume is 0
                holding_volume = holdings['volume']
                holding_avg_price = holdings['average_price']
                new_volume = holding_volume - trade_volume
                if new_volume == 0:
                    holding_avg_price = 0
                HoldingMapper().update_holdings(username,
                                                ticker_symbol,
                                                new_volume,
                                                holding_avg_price)
            else:
                # Unexpected transaction
                raise ValueError('Invalid transaction type')
        else:
            HoldingMapper().insert_holdings(username, ticker_symbol,
                                            trade_volume,
                                            trade_unit_price)

    def get_holding_volume(self, username, ticker_symbol):
        holding_volume = 0
        # TODO REPLACE MAPPER FUNCTION BY CLASS FUNCTION
        # holdings = self.get_user_holdings_by_symbol(username, ticker_symbol)
        holdings = HoldingMapper().select_holdings_by_symbol(username, ticker_symbol)
        if holdings is not None:
            holding_volume = holdings['volume']
        return holding_volume

    def get_user_holding_by_symbol(self, username, ticker_symbol):
        """Gets a specific ticker symbol's holding, for a specific account.

        Args:
            username (str): username's account to look for holding records.
            ticker_symbol (str): a specific ticker symbol to look for holding records.

        Returns:
            Holding: if a holding for 'ticker_symbol' is found for the account ('username').
            None: if the account associated with the 'username' has no holdings for 'ticker_symbol'.

        """

        result = HoldingMapper().select_holdings_by_symbol(username, ticker_symbol)
        if result is None:
            return None

        return self.__dict_to_holding(result)

    def get_user_holdings(self, username):
        """Gets all holdings of a specific account.

        Args:
            username (str): username associated with the account to look for holding records.

        Returns:
            Holding[]: if holdings are found for the account ('username').
            None: if not holdings are found.

        """
        result = HoldingMapper().select_holdings_by_username(username)

        if result is None:
            return None

        holdings = []
        for item in result:
            holdings.append(self.__dict_to_holding(item))

        return holdings

    def get_holdings_with_market_value(self, username):
        mkt_holding_list = None
        # TODO REPLACE MAPPER FUNCTION BY CLASS FUNCTION
        # user_holdings = self.get_user_holdings(username)
        user_holdings = HoldingMapper().select_holdings_by_username(username)
        if user_holdings is not None:
            mkt_holding_list = []
            # Generates an updated holding list containing market price info
            for item in user_holdings:
                # Gets updated market price
                quote = Quote.from_market_data(item['ticker_symbol'])
                # Creates and fills holdings dictionary with updated market info
                mkt_holding = {}
                mkt_holding['id'] = item['id']
                mkt_holding['username'] = item['username']
                mkt_holding['ticker_symbol'] = item['ticker_symbol']
                mkt_holding['volume'] = item['volume']
                mkt_holding['avg_buy_price'] = item['average_price']
                mkt_holding['mkt_price'] = quote.last_price
                ###### CALCULATES TOTALS AND DIFFERENCE ######
                # Total based on Buy Prices
                total_buy_price = item['volume'] * item['average_price']
                mkt_holding['total_buy_price'] = total_buy_price
                # Total based on Market Prices. Assumes one brokerage fee per holding.
                total_mkt_price = (
                    item['volume'] * quote.last_price) - Holding.BROKERAGE_FEE
                mkt_holding['total_mkt_price'] = total_mkt_price
                # Difference between market and buy price
                mkt_holding['difference'] = total_mkt_price - total_buy_price

                # Appends to the market holding list
                mkt_holding_list.append(mkt_holding)

        return mkt_holding_list
