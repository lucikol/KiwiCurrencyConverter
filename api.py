"""
Kiwi Currency Converter - Web API

Author: Lucie Koláriková
Date: February 2019
"""

from flask import request, Flask, jsonify
import currency_converter as cc

app = Flask(__name__)  # Creates the Flask application object


@app.route('/currency_converter', methods=['GET'])
def home():
    output_currency = ""
    if 'amount' in request.args and 'input_currency' in request.args:
        # Save the request arguments
        amount = float(request.args['amount'])
        input_currency = request.args['input_currency']
        if 'output_currency' in request.args:
            output_currency = request.args['output_currency']
    else:
        return "Wrong arguments."

    # Create the object for the conversion
    converter = cc.Converter(amount, input_currency, output_currency)
    try:
        # Convert the input currency to output currency
        return jsonify(converter.convert())
    except cc.RatesNotAvailableException as e:
        # Data for this conversion is not available
        return e.__str__()


def main():
    app.config["DEBUG"] = True
    app.run()


if __name__ == '__main__':
    main()
