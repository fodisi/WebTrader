#!/usr/bin/env python3

from flask import Blueprint, render_template, request, jsonify
import json

from ..model.holding import Holding
from ..serializer.holding_serializer import HoldingSerializer


holding_ctrl = Blueprint('holding', __name__, url_prefix='/holdings')


@holding_ctrl.route('/api/', methods=['GET'])
def api_holdings():

    # TODO Improve validations related to parameters.
    username = request.args.get('username')
    symbol = request.args.get('symbol')

    # At least the username must be provided. If not, returns error.
    if username is None:
        response = jsonify({
            "Error": "Missing required parameter 'username'.",
            "SupportedHoldingsEndpoints:": [
                {"UserHoldings": "/api/holdings/?username='username'"},
                {"UserHoldingsByTickerSymbol": "/api/holdings/?username='username'&symbol='symbol'"}
            ]
        })
        response.status_code = 400  # bad request
        return response

    try:
        if symbol is None:
            # Providing just username must return all user holdings.
            holdings = Holding().get_user_holdings(username)
            response = HoldingSerializer().jsonify(holdings, many=True)
        else:
            # Providing username and symbol must return symbol holding.
            holdings = Holding().get_user_holding_by_symbol(username, symbol)
            response = HoldingSerializer().jsonify(holdings)

        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"Error": e.args[0]})
        response.status_code = 500  # Server error
        return response
