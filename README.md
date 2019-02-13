# Kiwi Currency Converter
Currency Converter for Kiwi Junior Python Developer position. The project consists of command-line interface (CLI) application and web API application. The user fills the parameters listed below (input and output currency and amount) and the program prints the result of the conversion in JSON format.

## Prerequisites

You will need these modules: ```Flask, forex-python```

## Installing

Use: 
```pip install -r requirements.txt``` to install all required modules needed for the program to run succesfully.

## Parameters
- `amount` - amount which we want to convert - float
- `input_currency` - input currency - 3 letters name or currency symbol
- `output_currency` - requested/output currency - 3 letters name or currency symbol (optional)

## Functionality
- converts given amount of input currency to new amount of output currency and prints the result in JSON format 
- if output_currency param is missing, convert to all known currencies

## Usage examples:
### CLI application
Using currency codes for both input and output currencies:
```
python cli.py --amount 100.0 --input_currency EUR --output_currency CZK
{
    "input": {
        "amount": 100.0,
        "currency": "EUR"
    },
    "output": {
        "CZK": 2579.5
    }
}
```
Using currency code just for one currency and currency symbol for the other - there is an added item "symbol_currencies" in the JSON output containing list of all the currencies that use the given symbol (this is used only if the symbol belongs to more currencies):
```
python cli.py --amount 0.9 --input_currency ¥ --output_currency AUD
{
    "input": {
        "amount": 0.9,
        "currency": "CNY"
    },
    "output": {
        "AUD": 0.18711
    },
    "symbol_currencies": {
        "\u00a5": [
            "CNY",
            "JPY"
        ]
    }
}
```
Output currency is missing - converts to all known currencies + lists all the currencies that use the symbol £ (\u00a3):
```
python cli.py --amount 10.92 --input_currency £
{
    "input": {
        "amount": 10.92,
        "currency": "GBP"
    },
    "output": {
        "AUD": 19.83072,
        "BGN": 24.393096,
        ...
    },
    "symbol_currencies": {
        "\u00a3": [
            "GBP",
            "EGP",
            "FKP",
            "GIP",
            "LBP",
            "SHP"
        ]
    }
}

```

### Web API application
```
GET /currency_converter?amount=0.9&input_currency=¥&output_currency=AUD HTTP/1.1
{ "input": { "amount": 0.9, "currency": "CNY" }, "output": { "AUD": 0.18711 }, "symbol_currencies": { "\u00a5": [ "CNY", "JPY" ] } }
```

## Problems
- Converting to all known currencies takes some time due to implementation of forex-python module that opens the file for every conversion. New solution could be implemented that would save the file contents into a variable (or the module could be changed, but that is not in accordance with best practices).
- Due to the fact that more currencies use the same currency symbol the program could convert other currency than the user intended. As the best solution was chosen that the program lists all the currency codes for that given symbol because if the user chose typing the symbol for both input and output currency, the program could not generate clear output in JSON format that would show all the currency conversions.


## Built With

* [Flask](http://flask.pocoo.org/) - The web API framework used
* [forex-python](https://pypi.org/project/forex-python/) - Free exchange rates and currency conversion

## Authors

* **Lucie Koláriková** - [lucikol](https://github.com/lucikol)
