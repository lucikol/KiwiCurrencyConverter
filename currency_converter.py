"""
Kiwi Currency Converter

Author: Lucie Koláriková
Date: February 2019
"""

import getopt
import forex_python.converter
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
import sys
import os
import json

from urllib import request


class Converter:
    """
    Class representing the converter with input and output currencies and amount
    """
    def __init__(self, amount, input_code, output_code):
        self.amount = amount
        self.input_code = input_code    # Input currency code (e.g. EUR)
        self.output_code = output_code  # Output currency code
        self.input_symbol = ""
        self.output_symbol = ""
        self.currencies_symbols = {}

        self.check_currency_recognition()

    def __str__(self):
        return str(self.amount) + " " + self.input_code + " to " + self.output_code

    def get_currency_code_and_symbol(self, currency):
        """
        Checks the currency code, then the symbol and returns the symbol and code
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

                codes_for_symbol = self.get_codes_for_symbol(currency)
                if codes_for_symbol is None:
                    # The symbol is valid just for one currency
                    return cc.get_currency_code_from_symbol(currency), currency
                else:
                    # The symbol is valid for multiple currencies
                    return codes_for_symbol[0], currency

        return currency, None

    def check_currency_recognition(self):
        """"
        Checks if both input and output currency is distinguishable code or symbol and fills the input and output codes
        """
        self.input_code, self.input_symbol = self.get_currency_code_and_symbol(self.input_code)
        if self.output_code != "":
            self.output_code, self.output_symbol = self.get_currency_code_and_symbol(self.output_code)
        # Output currency is not set - convert to all known currencies

    def get_codes_for_symbol(self, symbol):
        """
        Returns list of currency codes with the given symbol
        """

        for item in self.currencies_symbols:
            for k, v in item.items():
                if k == symbol:
                    return v
        return None

    def convert(self):
        # Load the currency rates using Forex Python Converter
        cr = CurrencyRates()

        # Print the result of the conversion
        data = {}
        data['input'] = {'amount': self.amount, 'currency': self.input_code}
        data['output'] = {}

        file_path = os.path.dirname(os.path.abspath(forex_python.converter.__file__))
        with open(file_path + '/raw_data/currencies.json') as f:
            currency_data = json.loads(f.read())

            if self.output_code == "":
                for item in currency_data:
                    #print(item)
                    for k, v in item.items():
                        if k == "cc":
                            try:
                                data['output'].update({v: cr.convert(self.input_code, v, self.amount)})
                            except RatesNotAvailableError:
                                # Data for this currency conversion is not available, skip this conversion.
                                continue
            else:
                try:
                    data['output'] = {self.output_code: cr.convert(self.input_code, self.output_code, self.amount)}
                except RatesNotAvailableError:
                    print("Data for this currency conversion is not available.")

        json_data = json.dumps(data, indent=4, sort_keys=True)
        print(json_data)
        # print(cr.convert(converter.input_currency, converter.output_currency, converter.amount))
        if self.currencies_symbols:
            if self.input_symbol:
                self.__print_currencies_for_the_symbol(self.input_symbol)
            if self.output_symbol:
                self.__print_currencies_for_the_symbol(self.output_symbol)

    def __print_currencies_for_the_symbol(self, symbol):
        print("For the symbol " + symbol + " there are various currencies available: " +
              str(self.get_codes_for_symbol(symbol)))


def internet_on():
    """
    Checks the internet connection
    :return: True if the connection can be established
    """
    try:
        request.urlopen('http://google.com', timeout=1)
        return True
    except request.URLError:
        return False


def arguments_parse():
    """
    Parses the command line arguments
    :return: Converter object filled with arguments values
    """
    try:
        # Try getting the arguments
        opts, args = getopt.getopt(sys.argv[1:], "", ["amount=", "input_currency=", "output_currency="])
    except getopt.GetoptError:
        # Wrong arguments
        print("Wrong arguments.\n"
              "Usage example: python currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK")
        sys.exit(2)

    amount = 0
    input_currency = ""
    output_currency = ""

    for opt, val in opts:
        if opt == "--amount":
            amount = float(val)
        if opt == "--input_currency":
            input_currency = val
        if opt == "--output_currency":
            output_currency = val

    # Return the converter object filled with arguments values
    return Converter(amount, input_currency, output_currency)


def main():
    """
    Main function
    """
    # Check the internet connection
    if not internet_on():
        print("Connect to the internet to get the currency data.")
        # We can't get the currency data -- internet connection needed
        sys.exit(1)

    # Parse the arguments
    converter = arguments_parse()

    #print(converter.__str__())

    converter.convert()


if __name__ == '__main__':
    main()
