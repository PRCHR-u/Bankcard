from typing import List, Dict, Any, Generator

def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """Генератор для фильтрации транзакций по валюте."""
    for transaction in transactions:
        transaction_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Генератор для получения описаний транзакций."""
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """Генератор для генерации номеров банковских карт в заданном диапазоне."""
    if start < 1 or stop > 9999999999999999 or start > stop:
        raise ValueError("Invalid range for card numbers")
    for number in range(start, stop + 1):
        formatted_number = f"{number:016d}"
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"
