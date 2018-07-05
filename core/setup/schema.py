#!/usr/bin/env python3

import sqlite3


connection = sqlite3.connect('master.db', check_same_thread=False)
cursor = connection.cursor()

cursor.execute(
    """CREATE TABLE users(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(16) UNIQUE NOT NULL,
        password VARCHAR(32) NOT NULL,
        profile VARCHAR(1) NOT NULL,
        initial_balance FLOAT NOT NULL,
        cur_balance FLOAT NOT NULL
    );"""
)

cursor.execute(
    """CREATE TABLE holdings(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username varchar(16) NOT NULL,
        ticker_symbol VARCHAR(10) NOT NULL,
        volume INTEGER NOT NULL,
        average_price FLOAT NOT NULL,
        FOREIGN KEY(username) REFERENCES users(username),
        CONSTRAINT unique_username_ticker UNIQUE (username, ticker_symbol)
    );"""
)

cursor.execute(
    """CREATE TABLE orders(
        pk INTEGER PRIMARY KEY AUTOINCREMENT,
        username VARCHAR(16) NOT NULL,
        ticker_symbol VARCHAR(10) NOT NULL,
        date_time DATETIME NOT NULL,
        transaction_type BOOL NOT NULL,
        unit_price FLOAT NOT NULL,
        volume INTEGER NOT NULL,
        fee FLOAT NOT NULL,
        FOREIGN KEY(username) REFERENCES users(username)
    );"""
)

cursor.close()
connection.close()
