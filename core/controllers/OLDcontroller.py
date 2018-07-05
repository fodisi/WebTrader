#!/usr/bin/env python3

import core.model.model as model
import core.view as view


def balance(username):
    balance = model.get_current_balance(username)
    view.display_user_balance(username, balance)


def quote():
    ticker_symbol = view.quote_menu()
    last_price = model.get_last_price(ticker_symbol)
    view.display_last_price(last_price, True)


def lookup():
    company_name = view.lookup_menu()
    ticker_symbol = model.get_ticker_symbol(company_name)
    view.display_lookup(ticker_symbol, True)


def sell(username):
    (ticker_symbol, trade_volume) = view.sell_menu()
    order_status = model.sell(ticker_symbol,
                              int(trade_volume),
                              username)
    if order_status == 'SUCCESS':
        view.display_success()
    elif order_status == 'NO_FUNDS':
        holding_volume = model.get_holding_volume_by_symbol(
            username, ticker_symbol)
        view.display_insufficient_holdings(
            ticker_symbol, holding_volume)


def buy(username):
    ticker_symbol = view.buy_menu_ticker_symbol()
    # Gets the current price so can show it to user before buying it.
    last_price = model.get_last_price(ticker_symbol)
    view.display_last_price(last_price, False)

    trade_volume = view.buy_menu_volume_confirmation()
    order_status = model.buy(ticker_symbol,
                             int(trade_volume),
                             username)
    if order_status == 'SUCCESS':
        view.display_success()
    elif order_status == 'NO_FUNDS':
        balance = model.get_current_balance(username)
        view.display_insufficient_funds(balance)


def order_history(username):
    orders = model.get_order_history(username)
    view.display_order_history(username, orders)


# def user_dashboard(username):
#     holdings = model.get_holdings_by_username(username)
#     pl = model.get_realized_pl(username)
#     view.display_user_dashboard(username, holdings, pl)

def user_dashboard(username):
    pl = model.get_account_data_by_user(username)
    view.display_user_dashboard(username, pl)


def user_loop(username):
    first_access = True
    while True:
        try:
            if first_access:
                pl = model.get_account_data_by_user(username)
                if pl != None:
                    view.display_account_summary(pl, True, True)
                first_access = False

            current_balance = model.get_current_balance(username)
            user_input = view.main_user_menu(username, current_balance).lower()
            if user_input in ['b', 'buy']:
                buy(username)
            elif user_input in ['s', 'sell']:
                sell(username)
            elif user_input in ['l', 'lookup']:
                lookup()
            elif user_input in ['q', 'quote']:
                quote()
            elif user_input in ['a', 'balance']:
                balance(username)
            elif user_input in ['o', 'orders']:
                order_history(username)
            elif user_input in ['d', 'dashboard']:
                user_dashboard(username)
            elif user_input in ['e', 'exit']:
                view.exit_message()
                break
            else:
                view.display_invalid_menu_option()
        except Exception as e:
            view.display_error(e.args[0])


def admin_loop(username):
    while True:
        try:
            user_input = view.main_admin_menu(username).lower()
            if user_input == '1':
                create_user()
                view.display_success()
            elif user_input == '2':
                users = model.get_user_list()
                view.display_users(users)
            elif user_input == '3':
                user = view.delete_user_menu()
                if user != '':
                    if model.delete_user(user):
                        view.display_success()
                    else:
                        view.display_failure()
            elif user_input == '4':
                # leaderboard
                user_accounts = model.get_accounts_data()
                view.display_leaderboard(user_accounts)
                pass
            elif user_input == '0':
                view.exit_message()
                break
            else:
                view.display_invalid_menu_option()
        except Exception as e:
            view.display_error(e.args[0])


def login():
    username, pwd = view.login_menu()
    user = model.login(username, pwd)
    return user != None, user


def create_user():
    username, pwd = view.login_menu()
    model.create_user(username, pwd)


if __name__ == '__main__':
    while True:
        try:
            choice = view.main_global_menu()
            if choice == '1':
                status, user = login()
                if status:
                    username = user['username']
                    profile = user['profile']
                    if profile == 'U':
                        user_loop(username)
                    elif profile == 'A':
                        admin_loop(username)
                    else:
                        raise Exception('Invalid user profile.')
                else:
                    view.display_invalid_login()
            elif choice == '0':
                break
            else:
                view.display_invalid_menu_option()
        except Exception as e:
            view.display_error(e.args[0])
