import requests
from dotenv import load_dotenv
import os

load_dotenv()

EXCHANGE_RATES_API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
EXCHANGE_RATES_URL = "https://api.apilayer.com/exchangerates_data/latest"

def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Если валюта транзакции USD или EUR, обращается к внешнему API для получения курса.
    Иначе возвращает сумму транзакции в рублях.
    """
    try:
        amount = float(transaction.get("amount", 0.0))
    except ValueError:
        return 0.0

    currency = transaction.get("currency", "RUB").upper()

    if currency == "RUB":
        return amount

    headers = {
        "apikey": EXCHANGE_RATES_API_KEY
    }

    params = {
        "base": currency,
        "symbols": "RUB"
    }

    try:
        response = requests.get(EXCHANGE_RATES_URL, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        rate = data["rates"]["RUB"]
        return amount * rate
    except (requests.RequestException, KeyError, ValueError):
        return amount