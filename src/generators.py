from typing import Any, Dict, Generator, List


def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> Generator[Dict[str, Any], None, None]:
    """Генератор для фильтрации транзакций по валюте."""
    for transaction in transactions:
        transaction_currency = transaction.get("operationAmount", {}).get("currency", {}).get("code")
        if transaction_currency == currency:
            yield transaction


def transaction_descriptions(
        transactions: List[Dict[str, Any]]
) -> Generator[str, None, None]:
    """Генератор для получения описаний транзакций."""
    for transaction in transactions:
        description = transaction.get("description")
        if description:
            yield description


def card_number_generator(start: int, stop: int) -> Generator[str, None, None]:
    """
    Генератор для генерации номеров банковских карт в заданном диапазоне.

    :param start: Начальное значение диапазона (минимум 1).
    :param stop: Конечное значение диапазона (максимум 9999999999999999).
    :return: Генератор строк в формате XXXX XXXX XXXX XXXX.
    """
    if start < 1:
        raise ValueError("Start value must be at least 1")
    if stop > 9999999999999999:
        raise ValueError("Stop value must not exceed 9999999999999999")
    if start > stop:
        raise ValueError("Start value must be less than or equal to stop value")

    for number in range(start, stop + 1):
        # Преобразуем число в строку длиной 16 символов
        formatted_number = f"{number:016d}"
        # Разбиваем строку на группы по 4 цифры
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"
