#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, url_for, session

from ..model.user import User
from ..model.account import Account
from . import account_home


login_ctrl = Blueprint('login', __name__)


def try_login(username, password):
    user = User().login(username, password)
    return user != None


@login_ctrl.route('/', methods=['GET', 'POST'])
def show_login():
    if request.method == 'GET':
        return render_template('login.html', login_error='')
    else:
        username = request.form['email']
        password = request.form['password']
        if try_login(username, password):
            session['user'] = username
            return redirect(url_for('account_home.show_account_home'))
        else:
            session['user'] = ''
            return render_template('login.html', login_error='error')
