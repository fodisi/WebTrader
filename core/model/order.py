#!/usr/bin/env python3

from datetime import datetime

from core.mapper.order_mapper import OrderMapper
from core.model.user import User
from core.model.holding import Holding
from core.model.asset_quote import AssetQuote


class Order():

    def buy(self, ticker_symbol, trade_volume, username):
        user = User()
        user_balance = user.get_current_balance(username)
        quote = AssetQuote.from_market_data(ticker_symbol)
        transaction_cost = (quote.last_price * float(trade_volume)
                            ) + Holding.BROKERAGE_FEE
        if transaction_cost <= user_balance:
            # TODO Make inserts/updates in both tables be part of the same DB transaction.

            # Inserts order
            OrderMapper().insert_order(username,
                                       ticker_symbol,
                                       datetime.now(),
                                       'B',
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
        user = User()
        holding = Holding()
        user_balance = user.get_current_balance(username)
        holding_volume = holding.get_holding_volume(username, ticker_symbol)
        quote = AssetQuote.from_market_data(ticker_symbol)
        transaction_value = (quote.last_price * float(trade_volume)
                             ) - Holding.BROKERAGE_FEE

        if holding_volume >= trade_volume:
            # TODO Make inserts/updates in tables be part of the same DB transaction.

            # Inserts order
            OrderMapper().insert_order(username,
                                       ticker_symbol,
                                       datetime.now(),
                                       'S',
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
        return OrderMapper().select_order_history(username)
