#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session


home_ctrl = Blueprint('home', __name__, url_prefix='/home')


@home_ctrl.route('/', methods=['GET'])
def show_home():
    return render_template('home.html')

    # return __dashboard(session['user'])
