#!/usr/bin/env python3

import json

import requests


"""
Wrapper for MarkitOnDemmand API v2, available at http://dev.markitondemand.com/MODApis/Api/v2/doc.
"""


class AssetWrapper():

    def get_last_price(self, ticker_symbol):
        """Gets quote information for a specific ticker_symbol.
        RESPONSE FORMAT FROM THE API
        {"Status":"SUCCESS",
        "Name":"Tesla Inc",
        "Symbol":"TSLA",
        "LastPrice":335.07,
        "Change":-7.88,
        "ChangePercent":-2.29771103659425,
        "Timestamp":"Mon Jul 2 00:00:00 UTC-04:00 2018",
        "MSDate":43283,
        "MarketCap":56892875580,
        "Volume":18759765,
        "ChangeYTD":311.35,
        "ChangePercentYTD":7.61843584390556,
        "High":364.78,
        "Low":329.85,
        "Open":360.07}
        """
        try:
            # TODO Re-factor the following code so it doesn't just arbitrarily take the first
            endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='
            obj = json.loads(requests.get(endpoint + ticker_symbol).text)
            if obj['Status'] == 'SUCCESS':

                return json.loads(requests.get(endpoint + ticker_symbol).text)['LastPrice']
        except:
            msg = "Unable to get a price for symbol '{0}' on MarkitOnDemand API. Check your input and try again."
            raise Exception(msg.format(ticker_symbol))

    def get_ticker_symbol(self, company_name):
        # TODO Re-factor the following code so it doesn't just arbitrarily take the first
        """ RESPONSE FORMAT FROM THE API
        [{"Symbol":"TSLA","Name":"Tesla Inc","Exchange":"NASDAQ"}]
        """

        try:
            endpoint = 'http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input='
            return json.loads(requests.get(endpoint + company_name).text)[0]['Symbol']
        except:
            msg = "Unable to get a ticker symbol for company '{0}' on MarkitOnDemand API. Check your input and try again."
            raise Exception(msg.format(company_name))


if __name__ == '__main__':
    wrapper = AssetWrapper()
    print(wrapper.get_ticker_symbol('tesla'))
    print(wrapper.get_last_price('tsla'))
    print(wrapper.get_ticker_symbol('tesla154255'))
    print(wrapper.get_last_price('tsla154255'))
