#!/usr/bin/env python3


import json
import unittest

from core.serializer.markit_asset_decoder import MarkitOnDemmandAssetDecoder


class TestMarkitOnDemmandAssetDecoder(unittest.TestCase):
    """core.serializer.markit_asset_decoder.MarkitOnDemmandAssetDecoder tester unit."""

    def setUp(self):
        """Setup method executed before every test case."""
        self.markit_json_str = """{
            "Name": "name",
            "Symbol": "symbol",
            "Exchange": "exchange"
        }"""

        self.asset_dictionary = {
            "name": "name",
            "symbol": "symbol",
            "exchange": "exchange"
        }

    def test_decoder(self):
        """Tests MarkitOnDemmandAssetDecoder.convert method."""

        # Tests convert expecting a successfull decoding.
        json_obj = json.loads(self.markit_json_str,
                              cls=MarkitOnDemmandAssetDecoder)
        self.assertEqual(json_obj, self.asset_dictionary)
