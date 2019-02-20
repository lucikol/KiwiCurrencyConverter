"""
Kiwi Currency Converter

Author: Lucie Koláriková
Date: February 2019
"""


import forex_python.converter
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
import sys
import os
import json
from urllib import request


class RatesNotAvailableException(Exception):
    """
    Custom exception when rates for given currencies are not available
    """
    pass


class Converter:
    """
    Class representing the converter with input and output currencies and amount
    """
    def __init__(self, amount, input_code, output_code):
        self.amount = amount            # Amount of the currency to convert
        self.input_code = input_code    # Input currency code (e.g. EUR)
        self.output_code = output_code  # Output currency code
        self.input_symbol = ""          # Input symbol (e.g. $) - doesn't have to be set
        self.output_symbol = ""         # Output symbol - doesn't have to be set
        self.currencies_symbols = {}    # Dictionary (JSON) with currencies for given symbol

        # Checks input and output currency and eventually corrects the attributes
        self.__check_currency_recognition()

    def __str__(self):
        return str(self.amount) + " " + self.input_code + " to " + self.output_code

    def __get_currency_code_and_symbol(self, currency):
        """
        Checks the currency code, then the symbol and returns the  ode and the symbol
        :return: The currency code and currency symbol (if set, otherwise None)
        """
        # Load the currency codes
        cc = CurrencyCodes()

        if cc.get_symbol(currency) is None:
            # Currency code (e.g. EUR) is not recognized
            if cc.get_currency_code_from_symbol(currency) is None:
                # Currency symbol (e.g. $) is not recognized
                print("Currency " + currency + " not recognized.")
                sys.exit(1)
            else:
                # Currency symbol recognized
                file_path = os.path.dirname(os.path.abspath(__file__))
                with open(file_path + '/raw_data/currencies_symbols.json') as f:
                    self.currencies_symbols = json.loads(f.read())
                # Saves the list of codes for given symbol to variable
                codes_for_symbol = self.get_codes_for_symbol(currency)
                if codes_for_symbol is None:
                    # The symbol is valid just for one currency
                    # Returns the currency code and symbol
                    return cc.get_currency_code_from_symbol(currency), currency
                else:
                    # The symbol is valid for multiple currencies
                    # Returns the first currency code from the list and the currency symbol
                    return codes_for_symbol[0], currency

        # Returns currency code and no symbol (was not set)
        return currency, None

    def __check_currency_recognition(self):
        """"
        Checks if both input and output currency is distinguishable code or symbol and fills the input and output codes
        """
        self.input_code, self.input_symbol = self.__get_currency_code_and_symbol(self.input_code)
        if self.output_code != "":
            # Output currency set
            self.output_code, self.output_symbol = self.__get_currency_code_and_symbol(self.output_code)
        # Output currency is not set

    def __add_available_currencies_for_the_symbol(self, symbol, data):
        """Adds all available currency codes for particular symbol into the JSON format"""
        data['symbol_currencies'].update({symbol: self.get_codes_for_symbol(symbol)})

    def get_codes_for_symbol(self, symbol):
        """
        Gets list of currency codes with the given symbol
        :return: List of currency codes with the given symbol or None if the symbol belongs only to one currency
        """
        for item in self.currencies_symbols:
            for k, v in item.items():
                if k == symbol:
                    return v
        return None

    def convert(self):
        """
        Converts the input currency to the output currency.
        Raises RatesNotAvailableException if data for conversion is not available.
        :return: Currency conversion in JSON format
        """
        # Load the currency rates using Forex Python Converter
        cr = CurrencyRates()

        # Prepare the json format for printing the result of the conversion
        data = {}
        data['input'] = {'amount': self.amount, 'currency': self.input_code}
        data['output'] = {}

        file_path = os.path.dirname(os.path.abspath(forex_python.converter.__file__))
        with open(file_path + '/raw_data/currencies.json') as f:
            # Load the currency data to variable
            currency_data = json.loads(f.read())

        if self.output_code == "":
            # Output currency is not set - convert to all known currencies
            for item in currency_data:
                for k, v in item.items():
                    if k == "cc":
                        try:
                            data['output'].update({v: cr.convert(self.input_code, v, self.amount)})
                        except RatesNotAvailableError:
                            # Data for this currency conversion is not available, skip this conversion.
                            continue
        else:
            # Output currency is set
            try:
                data['output'] = {self.output_code: cr.convert(self.input_code, self.output_code, self.amount)}
            except RatesNotAvailableError:
                raise RatesNotAvailableException("Data for this currency conversion is not available.")

        if self.get_codes_for_symbol(self.input_symbol):
            # There is more currencies available for the input symbol
            data['symbol_currencies'] = {}
            self.__add_available_currencies_for_the_symbol(self.input_symbol, data)
        if self.get_codes_for_symbol(self.output_symbol):
            # There is more currencies available for the output symbol
            data['symbol_currencies'] = {}
            self.__add_available_currencies_for_the_symbol(self.output_symbol, data)

        return data


def internet_on():
    """
    Checks the internet connection
    :return: True if the connection can be established, False otherwise
    """
    try:
        request.urlopen('http://google.com', timeout=1)
        return True
    except request.URLError:
        return False
