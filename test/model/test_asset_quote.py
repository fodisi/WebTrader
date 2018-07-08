#!/usr/bin/env python3


import unittest
from datetime import datetime

from core.model.asset_quote import AssetQuote


class TestAssetQuote(unittest.TestCase):
    """core.model.asset_quote.AssetQuote tester unit."""

    def test_from_market_data(self):
        """Tests Model.AssetQuote.from_market_data method."""

        quote = AssetQuote.from_market_data('tsla')
        self.assertEqual(quote.symbol.lower(), 'tsla')
        self.assertNotEqual(quote.name, '')
        self.assertEqual(quote.exchange.upper(), 'NASDAQ')
        self.assertGreater(quote.last_price, 0)

    def test_str(self):
        """Tests Model.AssetQuote.__str__ custom method."""

        quote_dict = {
            'name': 'name',
            'symbol': 'symbol',
            'exchange': 'exchange',
            'last_price': 0.0,
            'change_1h': 0.0,
            'change_percent_1h': 0.0,
            'change_1d': 0.0,
            'change_percent_1d': 0.0,
            'change_7d': 0.0,
            'change_percent_7d': 0.0,
            'change_year': 0.0,
            'change_percent_year': 0.0,
            'timestamp': datetime.now(),
            'market_cap': 0,
            'volume': 0,
            'high': 0.0,
            'low': 0.0,
            'open': 0.0
        }

        quote_obj = AssetQuote()
        quote_obj.__dict__.update(quote_dict)
        self.assertEqual(str(quote_dict), str(quote_obj))
