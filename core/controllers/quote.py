#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core.model.asset_quote import AssetQuote

quote_ctrl = Blueprint('quote', __name__, url_prefix='/quote')

html_filename = 'quote.html'


def __quote(symbol):
    quote = None
    error = None
    try:
        quote = AssetQuote.from_market_data(symbol)
        quote = {'exchange': quote.exchange,
                 'symbol': quote.symbol,
                 'price': quote.last_price}
    except Exception as e:
        error = e.args[0]

    return render_template(html_filename, quote=quote, error=error)


@quote_ctrl.route('/', methods=['GET', 'POST'])
def show_quote():
    if request.method == 'GET':
        return render_template(html_filename)
    else:
        return __quote(request.form['symbol'])
