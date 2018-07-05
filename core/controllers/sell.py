#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session

from core.model.order import Order
from core.model.holding import Holding


sell_ctrl = Blueprint('sell', __name__, url_prefix='/sell')

html_filename = 'sell.html'


def __sell(symbol, volume, username):
    status = None
    error_detail = None
    try:
        # Executes the order and stores the status (SUCCESS or NO_FUNDS)
        status = Order().sell(symbol, int(volume), username)

        # If user doesn't have enought holdings, sets error_details with available balance.
        if status == 'NO_FUNDS':
            hold_volume = Holding().get_holding_volume(username, symbol)
            error_detail = {'symbol': symbol, 'hold_volume': hold_volume}
    except Exception as e:
        status = 'EXCEPTION'
        error_detail = e.args[0]

    return render_template(html_filename, status=status, error_detail=error_detail)


@sell_ctrl.route('/', methods=['GET', 'POST'])
def show_sell():
    # username = request.args.get('username')
    if request.method == 'GET':
        return render_template(html_filename, status='', error_detail='')
    else:
        return __sell(request.form['symbol'], request.form['volume'], session['user'])
