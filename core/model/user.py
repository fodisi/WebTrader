#!/usr/bin/env python3


from core.mapper.user_mapper import UserMapper

""" Functions for Users. """


class User:

    def create_user(self, username, password):
        return UserMapper().insert_user(username, password)

    def update_balance(self, username, balance):
        return UserMapper().update_balance(username, balance)

    def delete_user(self, username):
        return UserMapper().delete_user(username)

    def login(self, username, password):
        user = UserMapper().select_user(username)
        if user != None:
            if (user['username'] == username) and (user['password'] == password):
                return user
        return None

    def get_user_list(self):
        return UserMapper().select_all_users()

    def get_current_balance(self, username):
        return UserMapper().select_current_balance(username)

    def get_balance_for_pl(self, username):
        return UserMapper().select_balance_for_pl(username)
