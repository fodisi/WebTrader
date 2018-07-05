#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session

from core.model.order import Order

order_ctrl = Blueprint('order', __name__, url_prefix='/order')

html_filename = 'order.html'


def __order_history(username):
    orders = None
    error = None
    try:
        orders = Order().get_order_history(username)
    except Exception as e:
        error = e.args[0]

    return render_template(html_filename, orders=orders, error=error)


@order_ctrl.route('/', methods=['GET'])
def show_order():
    return __order_history(session['user'])
