#!/usr/bin/env python3

from datetime import datetime

from ..mapper.order_mapper import OrderMapper
from .user import User
from .holding import Holding
from .quote import Quote
from .order_type import OrderType


class Order():

    def __init__(self):
        self.id = 0
        self.username = ''
        self.ticker_symbol = ''
        self.datetime = datetime.now
        self.order_type = OrderType.NONE
        self.unit_price = 0.0
        self.volume = 0.0
        self.fee = 0.0

    @property
    def cost_proceeds(self):
        if self.order_type == OrderType.MARKET_BUY:
            return (self.unit_price * self.volume) + self.fee
        elif self.order_type == OrderType.MARKET_SELL:
            return (self.unit_price * self.volume) - self.fee
        else:
            return 0.0

    def buy(self, ticker_symbol, trade_volume, username):
        # TODO Refactor
        user = User()
        user_balance = user.get_current_balance(username)
        quote = Quote.from_market_data(ticker_symbol)
        transaction_cost = (quote.last_price * float(trade_volume)
                            ) + Holding.BROKERAGE_FEE
        if transaction_cost <= user_balance:
            # TODO Make inserts/updates in both tables be part of the same DB transaction.

            # Inserts order
            OrderMapper().insert_order(username,
                                       ticker_symbol,
                                       datetime.now(),
                                       int(OrderType.MARKET_BUY),
                                       quote.last_price,
                                       trade_volume,
                                       Holding.BROKERAGE_FEE)

            # Inserts/Updates holdings
            unit_cost = transaction_cost / float(trade_volume)
            Holding().update_holdings(username, ticker_symbol,
                                      trade_volume, unit_cost, 'B')

            # Updates balance
            # When buying, new balance must subtract transaction cost (including brokerage fee)
            new_balance = user_balance - transaction_cost
            user.update_balance(username, new_balance)

            return 'SUCCESS'
        else:
            # TODO Improve return so could show current balance and transaction cost.
            return 'NO_FUNDS'

    def sell(self, ticker_symbol, trade_volume, username):
        # TODO Refactor
        user = User()
        holding = Holding()
        user_balance = user.get_current_balance(username)
        holding_volume = holding.get_holding_volume(username, ticker_symbol)
        quote = Quote.from_market_data(ticker_symbol)
        transaction_value = (quote.last_price * float(trade_volume)
                             ) - Holding.BROKERAGE_FEE

        if holding_volume >= trade_volume:
            # TODO Make inserts/updates in tables be part of the same DB transaction.

            # Inserts order
            OrderMapper().insert_order(username,
                                       ticker_symbol,
                                       datetime.now(),
                                       int(OrderType.MARKET_SELL),
                                       quote.last_price,
                                       trade_volume,
                                       Holding.BROKERAGE_FEE)

            # Inserts/Updates holdings
            unit_price = transaction_value / float(trade_volume)
            holding.update_holdings(username, ticker_symbol,
                                    trade_volume, unit_price, 'S')

            # When selling, new balance must sum up transaction value, excluding fees
            new_balance = user_balance + \
                (transaction_value - Holding.BROKERAGE_FEE)
            user.update_balance(username, new_balance)

            return 'SUCCESS'
        else:
            # TODO Improve return so could show current balance and transaction cost.
            return 'NO_FUNDS'

    def get_order_history(self, username):
        orders = OrderMapper().select_order_history(username)

        if orders is None:
            return None

        result = []
        for item in orders:
            order = Order()
            order.__dict__.update(item)
            result.append(order)

        return result
