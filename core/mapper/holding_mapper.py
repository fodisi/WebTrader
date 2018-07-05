#!/usr/bin/env python3

from core.mapper.base_mapper import BaseMapper


class HoldingMapper(BaseMapper):

    def select_holdings_by_symbol(self, username, ticker_symbol):
        sql_cmd = """
            SELECT
                pk,
                username,
                ticker_symbol,
                volume,
                average_price
            FROM
                holdings
            WHERE
                username = '{username}'
            AND
                ticker_symbol = '{ticker_symbol}'
            ; """.format(
            username=username,
            ticker_symbol=ticker_symbol
        )
        result = self.execute_query(sql_cmd)

        if len(result) > 0:
            holding = {}
            row = result[0]
            holding['pk'] = row[0]
            holding['username'] = row[1]
            holding['ticker_symbol'] = row[2]
            holding['volume'] = row[3]
            holding['average_price'] = row[4]
            return holding
        else:
            return None

    def select_holdings_by_username(self, username):
        sql_cmd = """
            SELECT
                pk,
                username,
                ticker_symbol,
                volume,
                average_price
            FROM
                holdings
            WHERE
                username = '{username}'
            AND
                volume > 0
            ORDER BY
                volume DESC
            ; """.format(username=username)

        result = self.execute_query(sql_cmd)

        if len(result) > 0:
            holding_list = []
            for row in result:
                holding = {}
                holding['pk'] = row[0]
                holding['username'] = row[1]
                holding['ticker_symbol'] = row[2]
                holding['volume'] = row[3]
                holding['average_price'] = row[4]
                holding_list.append(holding)
            return holding_list
        else:
            return None

    def insert_holdings(self, username, ticker_symbol, volume, average_price):
        sql_cmd = """
            INSERT INTO
                holdings
            (
                username,
                ticker_symbol,
                volume,
                average_price
            )
            VALUES
            (
                '{username}',
                '{ticker_symbol}',
                {volume},
                {average_price}
            )
            ; """.format(
            username=username,
            ticker_symbol=ticker_symbol,
            volume=volume,
            average_price=average_price
        )
        self.execute_non_query(sql_cmd)
        return True

    def update_holdings(self, username, ticker_symbol, volume, average_price):
        sql_cmd = """
            UPDATE
                holdings
            SET
                volume = {volume},
                average_price = {average_price}
            WHERE
                username = '{username}'
            AND
                ticker_symbol = '{ticker_symbol}'
            ; """.format(
            username=username,
            ticker_symbol=ticker_symbol,
            volume=volume,
            average_price=average_price
        )
        self.execute_non_query(sql_cmd)
        return True
