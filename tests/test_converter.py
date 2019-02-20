"""
Tests of currency_converter.py
"""
import unittest
import currency_converter


class TestConverter(unittest.TestCase):  # (Instances of the TestCase class represent the logical test units)
    def test_converter(self):
        converter = currency_converter.Converter(100, 'EUR', 'CZK')
        data = converter.convert()
        self.assertFalse(data is None)
        self.assertTrue(data["input"]["amount"] == 100)
        self.assertTrue(data["input"]["currency"] == "EUR")
        self.assertTrue("CZK" in data["output"])

        converter = currency_converter.Converter(58.5, '$', 'CZK')
        data = converter.convert()
        self.assertFalse(data is None)
        self.assertTrue(data["input"]["amount"] == 58.5)
        self.assertTrue(data["input"]["currency"] == "CAD")   # $ symbol translated to currency code
        self.assertTrue("CZK" in data["output"])
        self.assertTrue("symbol_currencies" in data)

        converter = currency_converter.Converter(1.001, '¥', "")
        data = converter.convert()
        self.assertFalse(data is None)
        self.assertTrue(data["input"]["amount"] == 1.001)
        self.assertTrue(data["input"]["currency"] == "CNY")  # ¥ symbol converted to currency code
        self.assertTrue("CZK" in data["output"])             # output symbol missing - converted to all known currencies
        self.assertTrue("symbol_currencies" in data)

