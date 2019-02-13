"""
Kiwi Currency Converter - Command Line Interface

Author: Lucie Koláriková
Date: February 2019
"""

import getopt
import sys
import currency_converter as cc


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
              "Usage example: python cli.py --amount 100.0 --input_currency EUR --output_currency CZK")
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
    return cc.Converter(amount, input_currency, output_currency)


def main():
    """
    Main function
    """
    # Check the internet connection

    if not cc.internet_on():
        print("Connect to the internet to get the currency data.")
        # We can't get the currency data -- internet connection needed
        sys.exit(1)

    # Parse the arguments
    converter = arguments_parse()

    # print(converter.__str__())

    try:
        print(converter.convert())
    except cc.RatesNotAvailableException as e:
        print(e.__str__())


if __name__ == '__main__':
    main()
