#!/usr/bin/env python3

from datetime import datetime

from core.mapper.base_mapper import BaseMapper


class OrderMapper(BaseMapper):
    def insert_order(self,
                     username,
                     ticker_symbol,
                     date_time,
                     transaction_type,
                     unit_price,
                     volume,
                     fee):
        sql_cmd = """
            INSERT INTO
                orders
            (
                username,
                ticker_symbol,
                date_time,
                transaction_type,
                unit_price,
                volume,
                fee
            )
            VALUES
            (
                '{username}',
                '{ticker_symbol}',
                '{date_time}',
                '{transaction_type}',
                {unit_price},
                {volume},
                {fee}

            )
            ; """.format(
            username=username,
            ticker_symbol=ticker_symbol,
            date_time=date_time,
            transaction_type=transaction_type,
            unit_price=unit_price,
            volume=volume,
            fee=fee
        )
        self.execute_non_query(sql_cmd)
        return True

    def select_order_history(self, username):
        sql_cmd = """
            SELECT
                pk,
                username,
                ticker_symbol,
                strftime('%Y/%m/%d %H:%M:%S', date_time),
                transaction_type,
                unit_price,
                volume,
                fee
            FROM
                orders
            WHERE
                username = '{username}'
            ORDER BY
                date_time
            ; """.format(
            username=username)

        result = self.execute_query(sql_cmd)

        if len(result) > 0:
            order_list = []
            for row in result:
                order = {}
                order['pk'] = row[0]
                order['username'] = row[1]
                order['ticker_symbol'] = row[2]
                order['date_time'] = datetime.strptime(row[3],
                                                       '%Y/%m/%d  %H:%M:%S')
                order['order_type'] = row[4]
                order['unit_price'] = row[5]
                order['volume'] = row[6]
                order['fee'] = row[7]
                order_list.append(order)
            return order_list
        else:
            return None
