#!/usr/bin/env python3

import os
import getpass


def wait_for_user():
    print('\n\n\nPress ENTER to continue...')
    input()


def display_header():
    os.system('clear')
    # print('***********************')
    # print('**                   **')
    # print('*   Terminal Trader   *')
    # print('**                   **')
    # print('***********************\n')
    print(80 * '*')
    print('{0:^80}'.format('TERMINAL TRADER'))
    print(80 * '*')
    print('\n\n')


def display_error(error):
    display_header()
    print('\n\n\nAn ERROR ocurred:')
    print('\n{0}'.format('Invalid input'))
    print('\n{0}'.format('Details:'))
    print('\n{0}'.format(error))
    wait_for_user()


def display_success():
    display_header()
    print('\n\n\nOperation executed successfully.')
    wait_for_user()


def display_failure():
    display_header()
    print('\n\n\nUnable to execute operation due to invalid input or business constraints.')
    wait_for_user()


def display_invalid_menu_option():
    display_header()
    print('\n\n\nInvalid option. Try again.')
    wait_for_user()


def display_invalid_login():
    display_header()
    print('\n\n\nInvalid login.')
    wait_for_user()


def display_insufficient_funds(balance):
    display_header()
    print('\n\n\nInsufficient funds. Your balance is {0:.2f}.'.format(balance))
    wait_for_user()


def display_insufficient_holdings(ticker_symbol, holding_volume):
    display_header()
    msg = '\n\n\nInsufficient holdings.\nYour holding volume for "{0}" is "{1:.2f}".'
    print(msg.format(ticker_symbol, holding_volume))
    wait_for_user()


def display_user_balance(username, balance):
    display_header()
    print('\nUser: {0}'.format(username))
    print('Balance: {0:.2f}'.format(balance))
    wait_for_user()


def display_last_price(price, wait):
    # display_header()
    print('Quote: {0:.2f}'.format(price))
    if wait:
        wait_for_user()


def display_lookup(ticker_symbol, wait):
    # display_header()
    print('\nSymbol: {0}'.format(ticker_symbol))
    if wait:
        wait_for_user()


def display_users(users):
    display_header()

    if users != None:
        # Prints column headers
        pattern = '{0:<6} | {1:<15} | {2:^9} | {3:>15}'
        print(pattern.format('Id', 'Username', 'Profile', 'Balance'))

        # Prints column values
        pattern = '{0:06d} | {1:<15} | {2:^9} | {3:>15}'
        for user in users:
            print(pattern.format(user['pk'],
                                 user['username'],
                                 'Admin' if user['profile'] == 'A' else 'User',
                                 '{0:.2f}'.format(user['cur_balance'])))
    else:
        print('No user records available.')
    wait_for_user()


def display_order_history(username, orders):
    display_header()

    if orders != None:
        # Prints column headers
        pattern = '{0:<20} | {1:^6} | {2:^4} | {3:>5} | {4:>10} | {5:>10} | {6:>12}'
        print(pattern.format('Date', 'Symbol', 'Type', 'Fee',
                             'Unit Price', 'Volume', 'Trade Value*'))

        # Prints column values
        pattern = '{0:<20} | {1:^6} | {2:^4} | {3:>5} | {4:>10} | {5:>10} | {6:>12}'
        for order in orders:
            trade_value = order['volume'] * order['unit_price']
            print(pattern.format(order['date_time'].strftime('%Y/%m/%d %H:%M:%S'),
                                 order['ticker_symbol'],
                                 'Buy' if order['order_type'] == 'B' else 'Sell',
                                 '{0:.2f}'.format(order['fee']),
                                 '{0:.2f}'.format(order['unit_price']),
                                 '{0:.2f}'.format(order['volume']),
                                 '{0:.2f}'.format(trade_value)
                                 ))
        print('\n\nTrade Value*: =(Unit Price x Volume). No fees included.')
    else:
        print('No order records available for "{0}".'.format(username))
    wait_for_user()


def display_account_summary(pl, wait, header):
    if header:
        display_header()
        print('Check out your account summary!')

    cur_balance = pl['cur_balance']
    hold_buy_value = pl['buy_hold_value']
    account_real_value = pl['account_real_value']
    hold_mkt_value = pl['mkt_hold_value']
    account_mkt_value = pl['account_mkt_value']

    print('\n\n{0:^80}'.format('Summary'))
    print(80 * '-')
    print('Initial Balance:             {0:.2f}'.format(pl['initial_balance']))
    print('Current Balance:             {0:.2f}\n'.format(cur_balance))

    print('Holdings (Buy Price):        {0:.2f}'.format(
        hold_buy_value))
    print('Realized Account Value:      {0:.2f}'.format(
        account_real_value))
    label = 'Realized P/L | (%):          {0:.2f} ({1:.2f}%)\n'
    print(label.format(pl['real_pl_value'], pl['real_pl_percent']))

    print('Holdings (Market Price):     {0:.2f}'.format(
        hold_mkt_value))
    print('Unrealized Account Value:    {0:.2f}'.format(
        account_mkt_value))
    label = 'Unrealized P/L | (%):        {0:.2f} ({1:.2f}%)'
    print(label.format(pl['unreal_pl_value'], pl['unreal_pl_percent']))

    if wait:
        wait_for_user()


def display_user_dashboard(username, pl):
    display_header()

    print(80 * '-')
    title = 'Dashboard - User "{0}"'.format(username)
    print('{0:^80}'.format(title))
    print(80 * '-')

    if pl != None:

        display_account_summary(pl, False, False)

        holdings = pl['holdings']
        if holdings != None:
            # Prints section title
            print('\n\n{0:^80}'.format('Holdings'))
            print(80 * '-')
            # Prints column headers
            pattern = '{0:^6} | {1:>6} | {2:>10} | {3:>10} | {4:>10} | {5:>10} | {6:>10}'
            print(pattern.format('Symbol', 'Volume', 'Buy Price*',
                                 'Mkt Price*', 'Buy Total', 'Mkt Total', 'Difference'))

        # Prints column values
            pattern = '{0:^6} | {1:>6} | {2:>10} | {3:>10} | {4:>10} | {5:>10} | {6:>10}'
            for item in holdings:
                print(pattern.format(item['ticker_symbol'],
                                     '{0:.2f}'.format(item['volume']),
                                     '{0:.2f}'.format(item['avg_buy_price']),
                                     '{0:.2f}'.format(item['mkt_price']),
                                     '{0:.2f}'.format(item['total_buy_price']),
                                     '{0:.2f}'.format(item['total_mkt_price']),
                                     '{0:.2f}'.format(item['difference'])
                                     ))

            print('\n\n')
            print(80 * '-')
            print('Buy Price*: Average buy prices. Fees included.')
            print('Mkt. Price*: Fees included.')
        else:
            print('No holding records available for "{0}".'.format(username))

    else:
        print('No P/L data available for "{0}".'.format(username))

    wait_for_user()


def display_leaderboard(user_accounts):
    # TODO Refactor - this is UGLY
    display_header()

    print(80 * '-')
    print('{0:^80}'.format('Leaderboards'))
    print(80 * '-')

    if len(user_accounts) > 0:
        pattern = '{0:>2} | {1:<10} | {2:>12} | {3:>13} | {4:>10} | {5:>10}'

        realized_pl = sorted(
            user_accounts, key=lambda k: k['real_pl_value'], reverse=True)
        count = 10 if len(realized_pl) > 10 else len(realized_pl)

        # Prints section title
        print('\n\n{0:^80}'.format('Realized Profit / Loss'))
        print(80 * '-')
        print(pattern.format('#', 'Username', 'Cur. Balance', 'Account Value',
                             'P/L Value', 'P/L %'))
        # Prints columns
        for i in range(count):
            item = realized_pl[i]
            print(pattern.format(str(i + 1),
                                 item['username'],
                                 '{0:.2f}'.format(item['cur_balance']),
                                 '{0:.2f}'.format(item['account_real_value']),
                                 '{0:.2f}'.format(item['real_pl_value']),
                                 '{0:.2f}'.format(item['real_pl_percent'])
                                 ))

        unreal_pl = sorted(
            user_accounts, key=lambda k: k['unreal_pl_value'], reverse=True)
        count = 10 if len(unreal_pl) > 10 else len(unreal_pl)

        # Prints section title
        print('\n\n{0:^80}'.format('Unrealized Profit / Loss'))
        print(80 * '-')
        print(pattern.format('#', 'Username', 'Cur. Balance', 'Account Value',
                             'P/L Value', 'P/L %'))
        # Prints columns
        for i in range(count):
            item = unreal_pl[i]
            print(pattern.format(str(i + 1),
                                 item['username'],
                                 '{0:.2f}'.format(item['cur_balance']),
                                 '{0:.2f}'.format(item['account_mkt_value']),
                                 '{0:.2f}'.format(item['unreal_pl_value']),
                                 '{0:.2f}'.format(item['unreal_pl_percent'])
                                 ))

    else:
        print('No user accounts available.')
    wait_for_user()


def main_global_menu():
    display_header()
    print('\n\n\n1 - Login')
    # print('2 - Create user')
    print('0 - Exit')
    return input('\n\n\nType your choice:      ')


def main_admin_menu(username):
    display_header()
    print('Hello, {0}!'.format(username))
    print('\n\nChoose an option:')
    print('1 - Create user account')
    print('2 - List user accounts')
    print('3 - Delete user account')
    print('4 - Leaderboard')
    print('0 - Exit')
    return input('\n\nType your option:     ')


def main_user_menu(username, balance):
    display_header()
    print('Hello, {0}!'.format(username))
    print('Your balance is, {0:.2f}!'.format(balance))
    print('\n\nChoose an option:')
    print('b|buy       - Buy Stock')
    print('s|sell      - Sell Stock')
    print('l|lookup    - Lookup Stock Symbol')
    print('q|quote     - Stock Quote')
    print('a|balance   - Balance')
    print('o|orders    - Order History')
    print('d|dashboard - Dashboard (Summary + Holding Details)')
    print('e|exit      - Exit')
    return input('\n\nType your option:     ')


def login_menu():
    display_header()
    username = input('Login: ')
    pwd = getpass.getpass('Password: ')
    return username, pwd


def delete_user_menu():
    display_header()
    username = input('Username to be deleted: ')

    print('\nDeleting this user will also delete its orders and holdings history.')
    print('\nAre you sure you want to continue?')
    print('Type "yes" to delete the user or anything else to cancel.')

    if input('Confirm?     ').lower() != 'yes':
        username = ''

    return username


def buy_menu_ticker_symbol():
    display_header()
    ticker_symbol = input('Ticker Symbol: ')
    return ticker_symbol


def buy_menu_volume_confirmation():
    print('\nAlert: Stock quotes are subject to change.')
    print('By the time you confirm this operation, the updated market quote will be used to buy your stock.')
    trade_volume = input('\nTrade Volume: ')
    return trade_volume


def sell_menu():
    display_header()
    ticker_symbol = input('Ticker Symbol: ')
    trade_volume = input('Trade Volume: ')
    return ticker_symbol, trade_volume


def lookup_menu():
    display_header()
    company_name = input('Company Name: ')
    return company_name


def quote_menu():
    display_header()
    ticker_symbol = input('Ticker Symbol: ')
    return ticker_symbol


def exit_message():
    display_header()
    print('\n\n\nThanks for using Terminal Trader!')
    wait_for_user()


# def display_user_dashboard(username, holdings, pl):
#     display_header()

#     cur_balance = 0
#     holdings_total = 0

#     print(50 * '-')
#     title = 'Dashboard - User "{0}"'.format(username)
#     print('{0:^50}'.format(title))
#     print(50 * '-')

#     if pl != None:
#         # Prints section title
#         print('\n\n{0:^50}'.format('Balance and Profit/Loss (P/L)'))
#         print(50 * '-')
#         # Prints balance and realized PL.
#         print('Initial Balance:   {0:.2f}'.format(pl['initial_balance']))
#         print('Current Balance:   {0:.2f}'.format(pl['cur_balance']))
#         print('Realized P/L:      {0:.2f}'.format(pl['pl_value']))
#         print('Realized P/L (%):  {0:.2f}'.format(pl['pl_percent']))
#         cur_balance = pl['cur_balance']
#     else:
#         print('No balance available for "{0}".'.format(username))

#     if holdings != None:
#         # Prints section title
#         print('\n\n{0:^50}'.format('Holdings'))
#         print(50 * '-')
#         # Prints column headers
#         pattern = '{0:^6} | {1:>11} | {2:>10} | {3:>12}'
#         print(pattern.format('Symbol', 'Avg. Price*', 'Volume', 'Total'))

#         # Prints column values
#         pattern = '{0:^6} | {1:>11} | {2:>10} | {3:>12}'
#         for item in holdings:
#             total = item['volume'] * item['average_price']
#             print(pattern.format(item['ticker_symbol'],
#                                  '{0:.2f}'.format(item['average_price']),
#                                  '{0:.2f}'.format(item['volume']),
#                                  '{0:.2f}'.format(total)
#                                  ))
#             holdings_total += total

#         account_value = cur_balance + holdings_total
#         print('\n\n{0:^50}'.format('Summary'))
#         print(50 * '-')
#         print('Current Balance:          {0:.2f}'.format(cur_balance))
#         print('Total Holdings:           {0:.2f}'.format(holdings_total))
#         print('Realized Account Value*:  {0:.2f}'.format(account_value))

#         print('\n\n')
#         print(50 * '-')
#         print('Avg. Price*: Fees included.')
#         print('Realized Account Value*: Considering price paid for stocks.')
#     else:
#         print('No holding records available for "{0}".'.format(username))
#     wait_for_user()


# if __name__ == '__main__':
#     print(buy_menu())
