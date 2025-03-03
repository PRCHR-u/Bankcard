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
    amount = transaction.get("amount", 0)
    currency = transaction.get("currency", "RUB")

    if currency == "RUB":
        return amount

    try:
        # Предполагаем, что API возвращает курсы валют ОТНОСИТЕЛЬНО RUB
        response = requests.get("https://api.exchangerate-api.com/v4/latest/RUB")
        response.raise_for_status()
        rates = response.json().get("rates", {})
        rate = rates.get(currency, 1.0)
        return amount * rate

    except (requests.RequestException, KeyError):
        return amount  # Возвращаем исходную сумму при ошибках
