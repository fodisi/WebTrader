#!/usr/bin/env python3


import json
import unittest
from dateutil import parser

from core.serializer.markit_quote_decoder import MarkitOnDemandQuoteDecoder


class TestMarkitOnDemandQuoteDecoder(unittest.TestCase):
    """core.serializer.markit_quote_decoder.MarkitOnDemandQuoteDecoder tester unit."""

    def setUp(self):
        """Setup method executed before every test case."""
        self.markit_json_str = """{
            "Status": "SUCCESS",
            "Name": "name",
            "Symbol": "symbol",
            "LastPrice": 1.0,
            "Change": 1.0,
            "ChangePercent": 1.0,
            "Timestamp": "Mon Jan 1 02:30:40 UTC-04:00 2010",
            "MSDate": 1,
            "MarketCap": 1,
            "Volume": 1,
            "ChangeYTD": 1.0,
            "ChangePercentYTD": 1.0,
            "High": 1.0,
            "Low": 1.0,
            "Open": 1.0
        }"""

        self.quote_dictionary = {
            "name": "name",
            "symbol": "symbol",
            "exchange": "",
            "last_price": 1.0,
            "change_1h": 0.0,
            "change_percent_1h": 0.0,
            "change_1d": 1.0,
            "change_percent_1d": 1.0,
            "change_7d": 0.0,
            "change_percent_7d": 0.0,
            "change_year": 1.0,
            "change_percent_year": 1.0,
            "date_time": parser.parse("Mon Jan 1 02:30:40 UTC-04:00 2010"),
            "market_cap": 1,
            "volume": 1,
            "high": 1.0,
            "low": 1.0,
            "open": 1.0
        }

    def test_decoder(self):
        """Tests MarkitOnDemandQuoteDecoder.convert method."""

        # Tests convert expecting a successfull decoding.
        json_obj = json.loads(self.markit_json_str,
                              cls=MarkitOnDemandQuoteDecoder)
        self.assertEqual(json_obj, self.quote_dictionary)
