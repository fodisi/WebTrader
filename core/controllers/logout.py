#!/usr/bin/env python3

from flask import Blueprint, session, redirect, url_for


logout_ctrl = Blueprint('logout', __name__, url_prefix='/logout')


@logout_ctrl.route('/', methods=['GET', 'POST'])
def logout():
    # remove the username from the session if it is there
    session.pop('user', None)
    return redirect(url_for('login.show_login'))
