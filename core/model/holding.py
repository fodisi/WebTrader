#!/usr/bin/env python3


from core.model.asset import Asset
from core.mapper.holding_mapper import HoldingMapper


class Holding:
    BROKERAGE_FEE = 6.95

    def update_holdings(self, username, ticker_symbol, trade_volume, trade_unit_price, transaction_type):
        holdings = self.get_user_holdings_by_symbol(username, ticker_symbol)

        if holdings != None:
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
                raise Exception('Invalid transaction type')
        else:
            HoldingMapper().insert_holdings(username, ticker_symbol, trade_volume,
                                            trade_unit_price)

    def get_holding_volume(self, username, ticker_symbol):
        holding_volume = 0
        holdings = self.get_user_holdings_by_symbol(username, ticker_symbol)
        if holdings != None:
            holding_volume = holdings['volume']
        return holding_volume

    def get_user_holdings_by_symbol(self, username, ticker_symbol):
        return HoldingMapper().select_holdings_by_symbol(username, ticker_symbol)

    def get_user_holdings(self, username):
        return HoldingMapper().select_holdings_by_username(username)

    def get_holdings_with_market_value(self, username):
        mkt_holding_list = None
        user_holdings = self.get_user_holdings(username)
        if user_holdings != None:
            mkt_holding_list = []
            # Generates an updated holding list containing market price info
            for item in user_holdings:
                # Gets updated market price
                market_price = Asset().get_last_price(item['ticker_symbol'])
                # Creates and fills holdings dictionary with updated market info
                mkt_holding = {}
                mkt_holding['pk'] = item['pk']
                mkt_holding['username'] = item['username']
                mkt_holding['ticker_symbol'] = item['ticker_symbol']
                mkt_holding['volume'] = item['volume']
                mkt_holding['avg_buy_price'] = item['average_price']
                mkt_holding['mkt_price'] = market_price
                ###### CALCULATES TOTALS AND DIFFERENCE ######
                # Total based on Buy Prices
                total_buy_price = item['volume'] * item['average_price']
                mkt_holding['total_buy_price'] = total_buy_price
                # Total based on Market Prices. Assumes one brokerage fee per holding.
                total_mkt_price = (
                    item['volume'] * market_price) - Holding.BROKERAGE_FEE
                mkt_holding['total_mkt_price'] = total_mkt_price
                # Difference between market and buy price
                mkt_holding['difference'] = total_mkt_price - total_buy_price

                # Appends to the market holding list
                mkt_holding_list.append(mkt_holding)

        return mkt_holding_list
