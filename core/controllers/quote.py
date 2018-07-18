#!/usr/bin/env python3

from flask import Blueprint, render_template, request, jsonify
import json

from ..model.quote import Quote
from ..serializer.quote_serializer import QuoteSerializer


quote_ctrl = Blueprint('quote', __name__, url_prefix='/quotes')

html_filename = 'quote.html'


@quote_ctrl.route('/', methods=['GET', 'POST'])
def show_quote():
    if request.method == 'GET':
        return render_template(html_filename)
    else:
        try:
            quote = Quote.from_market_data(request.form['symbol'])
            result = QuoteSerializer().dump(quote).data
        except Exception as e:
            return render_template(html_filename, error=e.args[0])
        else:
            return render_template(html_filename, quote=result)


@quote_ctrl.route('/api/<symbol>', methods=['GET'])
def api_quote(symbol):
    try:
        quote = Quote.from_market_data(symbol)
        response = QuoteSerializer().jsonify(quote)
        response.status_code = 200
        return response
    except Exception as e:
        response = jsonify({"Error": e.args[0]})
        response.status_code = 500  # Server error
        return response
