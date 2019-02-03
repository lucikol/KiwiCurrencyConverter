"""
Kiwi Currency Converter

Author: Lucie Koláriková
Date: February 2019
"""

import getopt
from datetime import date
from forex_python.converter import CurrencyRates, CurrencyCodes, RatesNotAvailableError
import sys
import json

from urllib import request


class Converter:
    """
    Class representing the converter with input and output currencies and amount
    """
    def __init__(self, amount, input_currency, output_currency):
        self.amount = amount
        self.input_currency = input_currency    # Input currency code (e.g. EUR)
        self.output_currency = output_currency  # Output currency code

    def __str__(self):
        return str(self.amount) + " " + self.input_currency + " " + self.output_currency


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
              "Usage example: currency_converter.py --amount 100.0 --input_currency EUR --output_currency CZK")
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


def check_currency_code_or_symbol(currency, converter):
    """"

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
            if currency == converter.input_currency:
                # Change the input currency symbol to currency code
                converter.input_currency = cc.get_currency_code_from_symbol(currency)
            elif currency == converter.output_currency:
                # Change the output currency symbol to currency code
                converter.output_currency = cc.get_currency_code_from_symbol(currency)


def check_currency_recognition(converter):
    """"
    Checks if both input and output currency is distinguishable code or symbol
    """
    check_currency_code_or_symbol(converter.input_currency, converter)
    if converter.output_currency != "":
        check_currency_code_or_symbol(converter.output_currency, converter)
    # Output currency is not set - convert to all known currencies


def main():
    # Check the internet connection
    if not internet_on():
        print("Connect to the internet to get the currency data.")
        # We can't get the currency data -- internet connection needed
        sys.exit(1)

    # Load the currency rates using Forex Python Converter
    cr = CurrencyRates()

    # Parse the arguments
    converter = arguments_parse()

    check_currency_recognition(converter)

    print(converter.__str__())

    # Print the result of the conversion
    try:
        data = {}
        data['input'] = {'amount': converter.amount, 'currency': converter.input_currency}
        data['output'] = {converter.output_currency: cr.convert(converter.input_currency,
                                                                converter.output_currency, converter.amount)}
        json_data = json.dumps(data, indent=4, sort_keys=True)
        print(json_data)
        #print(cr.convert(converter.input_currency, converter.output_currency, converter.amount))
    except RatesNotAvailableError:
        print("Data for this currency conversion is not available.")


if __name__ == '__main__':
    main()
