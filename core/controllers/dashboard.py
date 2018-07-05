#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session

from core.model.account import Account


dashboard_ctrl = Blueprint('dashboard', __name__, url_prefix='/dashboard')


def __dashboard(username):
    pl = None
    error = None
    try:
        pl = Account().get_account_data_by_user(username)
    except Exception as e:
        error = e.args[0]

    return render_template('dashboard.html', pl=pl, error=error)


@dashboard_ctrl.route('/', methods=['GET'])
def show_dashboard():
    return __dashboard(session['user'])
