import re
from collections import Counter


def filter_by_description(transactions: list, search_string: str) -> list:
    """
    Возвращает список транзакций, у которых в описании есть строка поиска.

    Args:
        transactions: Список словарей с данными о банковских операциях.
        search_string: Строка поиска.

    Returns:
        Список словарей, у которых в описании есть строка поиска.
    """
    search_string = search_string.lower()
    filtered_transactions = [
        transaction for transaction in transactions
        if re.search(search_string, transaction.get("description", "").lower())
    ]
    return filtered_transactions


def categorize_transactions(transactions: list, categories: dict) -> dict:
    """
    Подсчитывает количество банковских операций каждого типа, используя Counter.

    Args:
        transactions: Список словарей с транзакциями.
        categories: Словарь для подсчета транзакций по описанию (ключ - описание, значение - количество).

    Returns:
        Обновленный словарь с результатами подсчета.
    """
    descriptions = [transaction.get("description", "Unknown") for transaction in transactions]
    counts = Counter(descriptions)

    for description, count in counts.items():
        categories[description] = categories.get(description, 0) + count

    return categories
