#!/usr/bin/env python3

import sqlite3


""" Migration needed due to changes in the model, switching from a str type
to enum(int) type, and preparing for future types of orders(OTC orders). """


connection = sqlite3.connect('master.db', check_same_thread=False)
cursor = connection.cursor()


# Sqlite does not allow to drop a column from a table, so it is needed to:
# 1. Create a new table orders_tmp.
# 2. Copy Buy records from orders to orders_tmp.
# 3. Copy Sell records from orders to orders_tmp.
# 4. Drop orders table.
# 5. Rename orders_tmp to orders.


# 1. Create a new table orders_tmp.
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS 
        orders_tmp
    (
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(16) NOT NULL,
        ticker_symbol VARCHAR(10) NOT NULL,
        date_time DATETIME NOT NULL,
        order_type INTEGER NOT NULL,
        unit_price FLOAT NOT NULL,
        volume INTEGER NOT NULL,
        fee FLOAT NOT NULL,
        FOREIGN KEY(username) REFERENCES users(username)
    );
    """
)

# 2. Copy Buy records from orders to orders_tmp.
# Copies orders with transaction_type = 'B' (Buys), inserting them with the value 0 to column order type.
cursor.execute(
    """
    INSERT INTO
        orders_tmp
    (
        username,
        ticker_symbol,
        date_time,
        order_type,
        unit_price,
        volume,
        fee
    )
    SELECT
        username,
        ticker_symbol,
        date_time,
        0,
        unit_price,
        volume,
        fee
    FROM
        orders
    WHERE
        transaction_type = 'B'
    ;
    """
)

# 3. Copy Sell records from orders to orders_tmp.
cursor.execute(
    """
    INSERT INTO
        orders_tmp
    (
        username,
        ticker_symbol,
        date_time,
        order_type,
        unit_price,
        volume,
        fee
    )
    SELECT
        username,
        ticker_symbol,
        date_time,
        1,
        unit_price,
        volume,
        fee
    FROM
        orders
    WHERE
        transaction_type = 'S'
    ;
    """
)

# Commits INSERTIONS before dropping the original table.
connection.commit()


# 4. Drop orders table.
cursor.execute("DROP TABLE IF EXISTS orders;")

# 5. Rename orders_tmp to orders.
cursor.execute("ALTER TABLE orders_tmp RENAME TO orders;")

cursor.close()
connection.close()
