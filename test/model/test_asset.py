#!/usr/bin/env python3


import unittest
from datetime import datetime

from core.model.asset import Asset


class TestAsset(unittest.TestCase):
    """core.model.asset.Asset unit tester."""

    def test_get_exchange_name(self):
        """Tests Model.Asset.get_exchange_name."""

        self.assertEqual(Asset.get_exchange_name('tsla').upper(), 'NASDAQ')

    def test_search_market_assets(self):
        """Tests Model.Quote.search_market_assets method."""

        assets = Asset.search_market_assets('corp')
        # Validates that list of assets has at least one item.
        self.assertGreater(len(assets), 0)
        # Validates that each asset symbol or name matches
        # the 'search_input' of search_market_assets method.
        for item in assets:
            match_symbol = item.symbol.lower().find('corp') >= 0
            match_name = item.name.lower().find('corp') >= 0
            self.assertTrue(match_name or match_symbol)
