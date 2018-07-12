#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session, jsonify

from ..model.order import Order
from ..serializer.order_serializer import OrderSerializer


order_ctrl = Blueprint('order', __name__)

html_filename = 'order.html'


@order_ctrl.route('/order', methods=['GET'])
def show_order():
    try:
        orders = Order().get_order_history(session['user'])
        result = OrderSerializer().dump(orders, many=True).data
    except Exception as e:
        return render_template(html_filename, error=e.args[0])
    else:
        return render_template(html_filename, orders=result)


@order_ctrl.route('/api/orders/<username>', methods=['GET'])
def api_orders(username):
    try:
        orders = Order().get_order_history(username)
    except Exception as e:
        return jsonify(e.args[0])
    else:
        return OrderSerializer().jsonify(orders, many=True)
