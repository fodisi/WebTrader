#!/usr/bin/env python3


import json
from dateutil import parser


class MarkitOnDemmandQuoteDecoder(json.JSONDecoder):
    """Decodes a MarkitOnDemmand JSON object to a Quote-compatible dictionary."""

    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.convert, *args, **kwargs)

    def convert(self, obj):
        """Converts a MarkitOnDemmand JSON object to a dictionary compatible with model.Quote.

        Args:
            - obj: MarkitOnDemmand JSON object

        Returns:
            (dictionary) a dictionary compatible with model.Quote.

        """

        if isinstance(obj, dict):
            try:
                return {
                    'name': obj['Name'],
                    'symbol': obj['Symbol'],
                    'exchange': '',
                    'last_price': obj['LastPrice'],
                    'change_1h': 0.0,
                    'change_percent_1h': 0.0,
                    'change_1d': obj['Change'],
                    'change_percent_1d': obj['ChangePercent'],
                    'change_7d': 0.0,
                    'change_percent_7d': 0.0,
                    'change_year': obj['ChangeYTD'],
                    'change_percent_year': obj['ChangePercentYTD'],
                    'date_time': parser.parse(obj['Timestamp']),
                    'market_cap': obj['MarketCap'],
                    'volume': obj['Volume'],
                    'high': obj['High'],
                    'low': obj['Low'],
                    'open': obj['Open']
                }
            except KeyError as k:
                msg = 'Invalid JSON object. Expected attributes not in place.\nDetails: {0}'
                raise ValueError(msg.format(k.args[0]))
            except Exception:
                raise
        else:
            raise TypeError('Invalid object type.')
