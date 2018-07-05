#!/usr/bin/env python3

from core.model.user import User
from core.model.holding import Holding


class Account():
    def get_realized_pl(self, username):
        initial, current = User().get_balance_for_pl(username)
        if initial > 0:
            pl = {}
            pl['username'] = username
            pl['initial_balance'] = initial
            pl['cur_balance'] = current
            pl['pl_value'] = current - initial
            pl['pl_percent'] = (current - initial) / initial * 100
            return pl
        else:
            return None

    def get_account_data_by_user(self, username):
        realized_pl = self.get_realized_pl(username)
        mkt_holdings = Holding().get_holdings_with_market_value(username)
        initial_balance = 0
        cur_balance = 0
        real_pl = 0
        real_pl_perc = 0
        hold_buy_value = 0
        hold_mkt_value = 0
        account_real_value = 0
        account_mkt_value = 0
        unrealized_pl = 0
        unrealized_pl_perc = 0

        if realized_pl != None:
            # Calculates account and PL data
            initial_balance = realized_pl['initial_balance']
            cur_balance = realized_pl['cur_balance']
            real_pl = realized_pl['pl_value']
            real_pl_perc = realized_pl['pl_percent']

        if mkt_holdings != None:
            hold_buy_value = sum(item['total_buy_price']
                                 for item in mkt_holdings)
            hold_mkt_value = sum(item['total_mkt_price']
                                 for item in mkt_holdings)
            account_real_value = cur_balance + hold_buy_value
            account_mkt_value = cur_balance + hold_mkt_value
            unrealized_pl = account_mkt_value - initial_balance
            unrealized_pl_perc = unrealized_pl / initial_balance * 100

        # Fills object with account and PL data to be returned
        pl_data = {}
        pl_data['username'] = username
        pl_data['initial_balance'] = initial_balance
        pl_data['cur_balance'] = cur_balance
        pl_data['buy_hold_value'] = hold_buy_value
        pl_data['mkt_hold_value'] = hold_mkt_value
        pl_data['account_real_value'] = account_real_value
        pl_data['account_mkt_value'] = account_mkt_value
        pl_data['real_pl_value'] = real_pl
        pl_data['real_pl_percent'] = real_pl_perc
        pl_data['unreal_pl_value'] = unrealized_pl
        pl_data['unreal_pl_percent'] = unrealized_pl_perc
        pl_data['holdings'] = mkt_holdings

        return pl_data

    def get_accounts_data(self):
        users = User().get_user_list()
        user_accounts = []
        for user in users:
            if user['profile'] == 'U':
                username = user['username']
                user_accounts.append(self.get_account_data_by_user(username))

        return user_accounts
