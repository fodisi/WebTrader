#!/usr/bin/env python3


import unittest
from datetime import datetime

from core.model.quote import Quote


class TestQuote(unittest.TestCase):
    """core.model.quote.Quote tester unit."""

    def test_set_exchange_from_market_data(self):
        """Tests Model.Quote.set_exchange_from_market_data."""

        quote = Quote()
        quote.symbol = 'tsla'
        quote.set_exchange_from_market_data()
        self.assertEqual(quote.exchange.upper(), 'NASDAQ')

    def test_from_market_data(self):
        """Tests Model.Quote.from_market_data method."""

        quote = Quote.from_market_data('tsla')
        self.assertEqual(quote.symbol.lower(), 'tsla')
        self.assertNotEqual(quote.name, '')
        self.assertEqual(quote.exchange.upper(), 'NASDAQ')
        self.assertGreater(quote.last_price, 0)
