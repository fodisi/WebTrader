#!/usr/bin/env python3

from flask import Blueprint, render_template, request, jsonify
import json

from ..model.quote import Quote
from ..serializer.quote_serializer import QuoteSerializer


quote_ctrl = Blueprint('quote', __name__)

html_filename = 'quote.html'


def __quote(symbol):
    quote = None
    error = None
    try:
        quote = Quote.from_market_data(symbol)
        result = {'exchange': quote.exchange,
                  'symbol': quote.symbol,
                  'price': quote.last_price}
    except Exception as e:
        error = e.args[0]

    return render_template(html_filename, quote=result, error=error)


@quote_ctrl.route('/quote', methods=['GET', 'POST'])
def show_quote():
    if request.method == 'GET':
        return render_template(html_filename)
    else:
        return __quote(request.form['symbol'])


@quote_ctrl.route('/api/quote/<symbol>', methods=['GET'])
def api_quote(symbol):
    try:
        quote = Quote.from_market_data(symbol)
        return QuoteSerializer().jsonify(quote)
    except Exception as e:
        return jsonify(e.args[0])
