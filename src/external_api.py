import os
from unittest.mock import MagicMock, patch

import requests
from dotenv import load_dotenv

load_dotenv()

EXCHANGE_RATES_API_KEY = os.getenv('EXCHANGE_RATES_API_KEY')
EXCHANGE_RATES_URL = "https://apilayer.com/exchangerates_data-api"

def convert_to_rub(transaction: dict) -> float:
    """
    Конвертирует сумму транзакции в рубли.
    Если валюта транзакции USD или EUR, обращается к внешнему API для получения курса.
    Иначе возвращает сумму транзакции в рублях.
    """
    try:
        amount = float(transaction.get("amount", 0))  # Преобразуем сумму в число
    except (TypeError, ValueError):
        return 0.0  # Возвращаем 0 при ошибке

    currency = transaction.get("currency", "RUB")

    if currency == "RUB":
        return amount

    try:
        # Запрашиваем курс валют относительно RUB
        headers = {
            "apikey": EXCHANGE_RATES_API_KEY
        }
        params = {
            "base": currency,
            "symbols": "RUB"
        }
        response = requests.get(EXCHANGE_RATES_URL, headers=headers, params=params)
        response.raise_for_status()
        rates = response.json().get("rates", {})
        rub_rate = rates.get("RUB", 1.0)  # Пример: {"RUB": 85.0}
        return round(amount * rub_rate, 2)
    except (requests.RequestException, KeyError):
        return amount
