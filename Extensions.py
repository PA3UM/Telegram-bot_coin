import requests
import json
from info import keys, apikey


class ConvertionException(Exception):
    pass

class CryptoConverter:
    @staticmethod
    def convert(quote, base, amount):

        quote_ticker, base_ticrer = keys[quote], keys[base]
        r = requests.get(
            f"https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticrer}&api_key={apikey}")
        total_base = json.loads(r.content)[keys[base]]
        if quote == base:
            raise ConvertionException(f'Не возможно конвероитовать одинаковые валюты {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        try:
            base_ticrer = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        return total_base

