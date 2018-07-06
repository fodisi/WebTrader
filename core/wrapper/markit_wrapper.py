#!/usr/bin/env python3


import json

import requests


class MarkitOnDemmand():
    """Wrapper for MarkitOnDemmand API, version 2, expecting JSON objects as result.

    Supported API Functions:
        - Quote: Quote information about a specific ticker symbol (stock).
        - Lookup: Basic ticker information (company name, symbol name and exchange).

    Note:
        API documentation available at: http://dev.markitondemand.com/MODApis/Api/v2/doc/.

    """

    # API url and version identifiers
    URL = 'http://dev.markitondemand.com/MODApis/Api'
    VERSION = 'v2'
    # API function identifiers
    FUNCTION_QUOTE = 'quote'
    FUNCTION_LOOKUP = 'lookup'
    FUNCTION_PARAMS = {FUNCTION_QUOTE: 'symbol', FUNCTION_LOOKUP: 'input'}

    @staticmethod
    def build_endpoint(api_function, param_value):
        """Creates the url to be used for calling a specific API endpoint.

        Args:
            api_call (str): The API function to be called.
            param (str): The parameter to be passed to the API function.

        Returns:
            The complete URL needed to call the specified API function.
        """

        if api_function.lower() not in MarkitOnDemmand.FUNCTION_PARAMS:
            raise ValueError('Invalid API function {}.'.format(api_function))

        # Expected API url format
        endpoint_format = '{url}/{version}/{function}/json?{param_name}={param_value}'
        return endpoint_format.format(url=MarkitOnDemmand.URL,
                                      version=MarkitOnDemmand.VERSION,
                                      function=api_function.lower(),
                                      param_name=MarkitOnDemmand.FUNCTION_PARAMS[api_function],
                                      param_value=param_value
                                      )

    @staticmethod
    def quote(ticker_symbol):
        """Gets quote information for a specific ticker symbol.

        API function name: Quote.

        API function endpoint: http://dev.markitondemand.com/MODApis/Api/v2/Quote/json?symbol='ticker_symbol'.

        Args:
            ticker_symbol (str): ticker symbol to look for a quote.

        Returns:
            string: quote information for a specific 'ticker_symbol', as a JSON object:
                {
                "Status":"SUCCESS",
                "Name":string,
                "Symbol":string,
                "LastPrice":float,
                "Change":float,
                "ChangePercent":float,
                "Timestamp":string, representing datetime in format "ddd MMM d HH:mm:ss UTCzzzzz yyyy",
                "MSDate":integer,
                "MarketCap":integer,
                "Volume":integer,
                "ChangeYTD":float,
                "ChangePercentYTD":float,
                "High":float,
                "Low":float,
                "Open":float
                }

        Raises:
            ValueError: if 'ticker_symbol' is empty or does not correspond to a valid ticker symbol.

        """

        # Successfull API call returns a JSON object that contains a field 'Status'.
        # API Calls passing an empty/invalid parameter return a JSON object with a field 'Message'.
        #
        # Invalid Symbol: {
        #   "Message":"No symbol matches found for tsla2.
        #   Try another symbol such as MSFT or AAPL, or use the Lookup API."
        # }
        # Missing Symbol: {
        #   "Message":"Missing Required Parameter: \"symbol\""
        # }

        # Creates and call API endpoint, then loads result into json result object.
        endpoint = MarkitOnDemmand.build_endpoint(MarkitOnDemmand.FUNCTION_QUOTE,
                                                  ticker_symbol)

        result = requests.get(endpoint)
        if not result.ok:
            result.raise_for_status()

        json_obj = json.loads(result.text)

        if 'Status' in json_obj:
            return json_obj

        if 'Message' in json_obj:
            raise ValueError(json_obj['Message'])

        # Should not arrive to this point.
        # If it does, an unsupported JSON object was returned from the API.
        raise TypeError("""Unsupported JSON object returned.
                        \nEndpoint: '{endpoint}'
                        \nJSON Object: {json_object}
                        """.format(endpoint=endpoint, json_object=json_obj))

    @staticmethod
    def lookup(search_input):
        """Gets lookup information for a specific 'input'.

        API function name: Lookup.

        API function endpoint: http://dev.markitondemand.com/MODApis/Api/v2/Lookup/json?input='search_input'.

        Args:
            search_input (str): input text to search for.

        Returns:
            None: if no content was found based on 'search_input'. Otherwise;
            string: a JSON object with lookup data, in the following format:
            [
                {
                "Symbol":string,
                "Name":string,
                "Exchange":string
                }
                , ...
            ]

        Raises:
            ValueError: if an error message is returned from the API.

        """

        # Successfull API call returns a JSON object that contains a field 'Status'.
        # API Calls passing an empty/invalid parameter return a JSON object with a field 'Message'.
        # {"Message":"Missing Required Parameter: \"input\""}

        # Creates and call API endpoint, then loads result into json result object.
        endpoint = MarkitOnDemmand.build_endpoint(MarkitOnDemmand.FUNCTION_LOOKUP,
                                                  search_input)

        result = requests.get(endpoint)
        if not result.ok:
            result.raise_for_status()

        json_obj = json.loads(result.text)

        if 'Message' in json_obj:
            raise ValueError(json_obj['Message'])

        return json_obj if (len(json_obj) > 0) else None
