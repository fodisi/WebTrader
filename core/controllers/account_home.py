#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session


account_home_ctrl = Blueprint('account_home', __name__, url_prefix='/home')


@account_home_ctrl.route('/', methods=['GET'])
def show_account_home():
    return render_template('account_home.html')

    # return __dashboard(session['user'])
