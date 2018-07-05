#!/usr/bin/env python3

from flask import Blueprint, render_template, request

from core.model.asset import Asset

quote_ctrl = Blueprint('quote', __name__, url_prefix='/quote')

html_filename = 'quote.html'


def __quote(symbol):
    quote = None
    error = None
    try:
        price = Asset().get_last_price(symbol)
        quote = {'symbol': symbol, 'price': price}
    except Exception as e:
        error = e.args[0]

    return render_template(html_filename, quote=quote, error=error)


@quote_ctrl.route('/', methods=['GET', 'POST'])
def show_quote():
    if request.method == 'GET':
        return render_template(html_filename)
    else:
        return __quote(request.form['symbol'])
