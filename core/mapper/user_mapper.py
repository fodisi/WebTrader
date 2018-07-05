#!/usr/bin/env python3


from core.mapper.base_mapper import BaseMapper

""" Functions for manipulating data from Users table. """


class UserMapper(BaseMapper):
    def select_user(self, username):
        sql_cmd = """
            SELECT 
                pk,
                username,
                password,
                profile,
                initial_balance,
                cur_balance
            FROM
                users
            WHERE
                username = '{username}'
            ; """.format(
            username=username
        )
        result = self.execute_query(sql_cmd)

        if len(result) > 0:
            user = {}
            row = result[0]
            user['pk'] = row[0]
            user['username'] = row[1]
            user['password'] = row[2]
            user['profile'] = row[3]
            user['initial_balance'] = row[4]
            user['cur_balance'] = row[5]
            return user
        else:
            return None

    def select_all_users(self):
        sql_cmd = """
            SELECT
                pk,
                username,
                password,
                profile,
                initial_balance,
                cur_balance
            FROM
                users
            ;"""

        result = self.execute_query(sql_cmd)

        if len(result) > 0:
            user_list = []
            for row in result:
                user = {}
                user['pk'] = row[0]
                user['username'] = row[1]
                user['password'] = row[2]
                user['profile'] = row[3]
                user['initial_balance'] = row[4]
                user['cur_balance'] = row[5]
                user_list.append(user)
            return user_list
        else:
            return None

    def select_current_balance(self, username):
        sql_cmd = """
            SELECT
                cur_balance
            FROM
                users
            WHERE
                username = '{username}'
            ; """.format(
            username=username
        )
        result = self.execute_query(sql_cmd)

        if len(result) > 0:
            row = result[0]
            return row[0]
        else:
            return 0

    def select_balance_for_pl(self, username):
        sql_cmd = """
            SELECT
                initial_balance,
                cur_balance
            FROM
                users
            WHERE
                username = '{username}'
            ; """.format(username=username)

        result = self.execute_query(sql_cmd)

        if len(result) > 0:
            row = result[0]
            # Returns: initial balance | current balance
            return row[0], row[1]
        else:
            return 0, 0

    def update_balance(self, username, balance):
        sql_cmd = """
            UPDATE
                users
            SET
                cur_balance = {balance}
            WHERE
                username = '{username}'
            ; """.format(
            username=username,
            balance=balance
        )
        self.execute_non_query(sql_cmd)
        return True

    def insert_user(self, username, password):
        sql_cmd = """
            INSERT INTO
                users
            (
                username,
                password,
                profile,
                initial_balance,
                cur_balance
            )
            VALUES
            (
                '{username}',
                '{password}',
                'U',
                100000,
                100000

            )
            ; """.format(
            username=username,
            password=password
        )
        self.execute_non_query(sql_cmd)
        return True

    def delete_user(self, username):
        # TODO Make all SQL commands execute in the same DB transaction.

        user = self.select_user(username)
        if user == None:
            return False

        if user['profile'] == 'A':
            return False

        # Deletes all user orders
        sql_cmd = "DELETE FROM orders WHERE username='{0}'".format(username)
        self.execute_non_query(sql_cmd)

        # Deletes all holdings
        sql_cmd = "DELETE FROM holdings WHERE username='{0}'".format(username)
        self.execute_non_query(sql_cmd)

        # Deletes user
        sql_cmd = "DELETE FROM users WHERE username='{0}'".format(username)
        self.execute_non_query(sql_cmd)

        return True
