#!/usr/bin/env python3

from flask import Blueprint, render_template, request, session

from ..model.order import Order
from ..model.user import User


buy_ctrl = Blueprint('buy', __name__, url_prefix='/buy')

html_filename = 'buy.html'


def __buy(symbol, volume, username):
    status = None
    error_detail = None
    try:
        # Executes the order and stores the status (SUCCESS or NO_FUNDS)
        status = Order().buy(symbol, int(volume), username)

        # TODO Make user see details about the transaction cost.
        # If user doesn't have enough funds, sets error_details  available balance.
        if status == 'NO_FUNDS':
            error_detail = User().get_current_balance(username)
    except Exception as e:
        status = 'EXCEPTION'
        error_detail = e.args[0]

    return render_template(html_filename, status=status, error_detail=error_detail)


@buy_ctrl.route('/', methods=['GET', 'POST'])
def show_buy():
    if request.method == 'GET':
        return render_template(html_filename, status='', error_detail='')
    else:
        return __buy(request.form['symbol'], request.form['volume'], session['user'])


# @buy_ctrl.route('/api/', methods=['POST'])
# def api_buy():
#     # TODO Improve validations related to parameters.
#     symbol = request.args.get('symbol')
#     volume = request.args.get('volume')

#     # At least the username must be provided. If not, returns error.
#     error = {}
#     if symbol is None:
#         error["SymbolError"] = "Missing required parameter 'symbol'."
#     if volume is None:
#         error["VolumeError"] = "Missing required parameter 'volume'."
#     try:
#         volume = float(volume)

#         response = jsonify({
#             "Error": '',
#             "SupportedHoldingsEndpoints:": [
#                 {"UserHoldings": "/api/holdings/?username='username'"},
#                 {"UserHoldingsByTickerSymbol": "/api/holdings/?username='username'&symbol='symbol'"}
#             ]
#         })
#         response.status_code = 400  # bad request
#         return response

#     try:

#         response.status_code = 200
#         return response
#     except Exception as e:
#         response = jsonify({"Error": e.args[0]})
#         response.status_code = 500  # Server error
#         return response
