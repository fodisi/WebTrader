#!/usr/bin/env python3

from datetime import datetime

from ..mapper.order_mapper import OrderMapper
from .user import User
from .holding import Holding
from .quote import Quote
from .order_type import OrderType


class Order():
    """Represents an order to buy or sell a specific asset (stock, currency, etc.).

    Attributes:
        id (int): the order id.
        username (str): the username placing the order.
        ticker_symbol (str): the asset ticker symbol.
        date_time (datetime): the date/time the order is/was placed.
        order_type (OrderType): indicates if the order is a buy or sell order.
        unit_price (float): the unit price paid for the asset.
        volume (float): the asset volume that is/was bought or sold.
        fee (float): the fee paid for placing the order.

    """

    def __init__(self,
                 id_=0,
                 username='',
                 ticker_symbol='',
                 date_time=datetime.now,
                 order_type=OrderType.NONE,
                 unit_price=0.0,
                 volume=0.0,
                 fee=0.0
                 ):
        """Class constructor. Initializes attributes with specified or default values.

        Args:
            id (int): the order id.
            username (str): the username placing the order.
            ticker_symbol (str): the asset ticker symbol.
            date_time (datetime): the date/time the order is/was placed.
            order_type (OrderType): indicates if the order is a buy or sell order.
            unit_price (float): the unit price paid for the asset.
            volume (float): the asset volume that is/was bought or sold.
            fee (float): the fee paid for placing the order.

        """

        self.id = id_
        self.username = username
        self.ticker_symbol = ticker_symbol
        self.date_time = date_time
        self.order_type = order_type
        self.unit_price = unit_price
        self.volume = volume
        self.fee = fee

    @property
    def cost_proceeds(self):
        """Represents the total cost/proceeds of an order.

        Calculation formula according to order type:
            Buy  : cost/proceeds = (unit_price * volume) + fee;
            Sell : cost/proceeds = (unit_price * volume) - fee;

        """
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
        """Gets the order history of a specific user, determined by 'username'.

        Args:
            username(str): username to be used when looking for order history.

        Returns:
            None: if 'username' has no record in its order history.
            Order[]: A list containing all orders placed by the 'username'.
        """

        orders = OrderMapper().select_order_history(username)

        if orders is None:
            return None

        result = []
        for item in orders:
            order = Order()
            order.__dict__.update(item)
            result.append(order)

        return result
