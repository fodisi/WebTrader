#!/usr/bin/env python3

from abc import ABC
import sqlite3 as db


class BaseMapper(ABC):
    def execute_non_query(self, sql_command):
        # creates a connection to the database
        with db.connect('master.db', check_same_thread=False) as conn:
            cursor = conn.cursor()
            """SQLite3 requires that this command be executed to active
            Foreign Key constrains
            Link: https://www.sqlite.org/foreignkeys.html#fk_enable"""
            cursor.execute("PRAGMA foreign_keys = ON;")
            # executes and commits the sql command
            cursor.execute(sql_command)
            conn.commit()
            cursor.close()

    def execute_query(self, sql_command):
        # creates a connection to the database
        with db.connect('master.db', check_same_thread=False) as conn:
            cursor = conn.cursor()
            # executes sql command and returns fetched data
            cursor.execute(sql_command)
            return cursor.fetchall()
