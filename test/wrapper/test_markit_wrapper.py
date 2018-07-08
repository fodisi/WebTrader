#!/usr/bin/env python3

import unittest

from core.wrapper.markit_wrapper import MarkitOnDemmand as wrapper


class TestMarkitOnDemmandWrapper(unittest.TestCase):
    """core.wrapper.markit_wrapper.MarkitOnDemmandWrapper unit tester."""

    def test_build_endpoint(self):
        """Tests MarkitOnDemmand.build_endpoint(Quote | Lookup |Invalid function name)."""

        # Tests QUOTE endpoint.
        expected = 'http://dev.markitondemand.com/MODApis/Api/v2/quote/json?symbol=tsla'
        result = wrapper.build_endpoint(wrapper.FUNCTION_QUOTE, 'tsla')
        self.assertEqual(result,
                         expected,
                         'Invalid QUOTE endpoint "{}"'.format(result))

        # Tests LOOKUP endpoint.
        expected = 'http://dev.markitondemand.com/MODApis/Api/v2/lookup/json?input=TESLA'
        result = wrapper.build_endpoint(wrapper.FUNCTION_LOOKUP, 'TESLA')
        self.assertEqual(result,
                         expected,
                         'Invalid LOOKUP endpoint "{}"'.format(result))

        # Tests for an invalid function name.
        with self.assertRaises(ValueError) as v:
            wrapper.build_endpoint('quote2', 'ANYTHING')
        self.assertTrue(v.exception.args[0].lower().startswith('invalid api'))

    def test_quote(self):
        """Tests MarkitOnDemmand.quote(Valid Symbol | Invalid Symbol | Missing Symbol)."""

        # Tests for a request with a valid symbol.
        result = wrapper.quote('tsla')
        self.assertIn('symbol', result)
        self.assertEqual(result['symbol'].lower(), 'tsla')

        # Tests for a request with an invalid symbol.
        with self.assertRaises(ValueError) as invalid:
            wrapper.quote('INVALID')
        self.assertTrue(
            invalid.exception.args[0].lower().startswith('no symbol'))

        # Tests for a request with an empty/missing symbol.
        with self.assertRaises(ValueError) as empty:
            wrapper.quote('')
        self.assertTrue(
            empty.exception.args[0].lower().startswith('missing required parameter'))

    def test_lookup(self):
        """Tests MarkitOnDemmand.lookup(Valid Input | Invalid Input | Missing Input)."""

        # Tests for a request with a valid input.
        result = wrapper.lookup('tesla')
        self.assertGreater(len(result), 0)

        # Tests for a request with a invalid input.
        result = wrapper.lookup('INVALID_INPUT')
        self.assertIsNone(result)

        # Tests for a request with an empty input.
        with self.assertRaises(ValueError) as invalid:
            wrapper.lookup('')
        self.assertTrue(
            invalid.exception.args[0].lower().startswith('missing required parameter'))

    def test_lookup_exchange(self):
        """Tests MarkitOnDemmand.lookup_exchange(Valid Symbol | Invalid Symbol | Missing Symbol)."""

        # Tests for a request with a valid ticker symbol.
        result = wrapper.lookup_exchange('tsla')
        self.assertEqual(result.upper(), 'NASDAQ')

        # Tests for a request with a invalid input.
        result = wrapper.lookup_exchange('INVALID_INPUT')
        self.assertIsNone(result)

        # Tests for a request with an empty input.
        with self.assertRaises(ValueError) as invalid:
            wrapper.lookup_exchange('')
        self.assertTrue(
            invalid.exception.args[0].lower().startswith('missing required parameter'))
