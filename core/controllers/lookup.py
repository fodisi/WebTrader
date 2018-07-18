#!/usr/bin/env python3

from flask import Blueprint, render_template, request, jsonify

from ..model.asset import Asset
from ..serializer.asset_serializer import AssetSerializer


lookup_ctrl = Blueprint('lookup', __name__, url_prefix='/lookup')

html_filename = 'lookup.html'


@lookup_ctrl.route('/', methods=['GET', 'POST'])
def show_lookup():
    if request.method == 'GET':
        return render_template(html_filename)
    else:
        try:
            lookups = Asset.search_market_assets(request.form['search_input'])
            result = AssetSerializer().dump(lookups, many=True).data
        except Exception as e:
            return render_template(html_filename, error=e.args[0])
        else:
            return render_template(html_filename, assets=result)


@lookup_ctrl.route('/api/<search_input>', methods=['GET'])
def api_lookup(search_input):
    try:
        assets = Asset.search_market_assets(search_input)
        return AssetSerializer().jsonify(assets, many=True)
    except Exception as e:
        return jsonify(e.args[0])
