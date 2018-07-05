#!/usr/bin/env python3

from flask import Blueprint, render_template, request, redirect, url_for, session

from core.model.user import User
from core.model.account import Account
from core.controllers import dashboard


login_ctrl = Blueprint('login', __name__)


def try_login(username, password):
    user = User().login(username, password)
    return user != None, user


@login_ctrl.route('/', methods=['GET', 'POST'])
def show_login():
    if request.method == 'GET':
        return render_template('login.html', login_error='')
    else:
        username = request.form['email']
        password = request.form['password']
        result, user = try_login(username, password)
        if result:
            # return redirect(url_for('dashboard.show_dashboard',
            #                         username=user["username"]))
            session['user'] = username
            session['francis'] = username
            return redirect(url_for('dashboard.show_dashboard'))
        else:
            session['user'] = ''
            return render_template('login.html', login_error='error')
