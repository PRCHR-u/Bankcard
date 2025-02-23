import logging
import re
from functools import wraps
from typing import Any, Dict, Generator, List

from black import datetime


def log(filename=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Configure logging
            logger = logging.getLogger(func.__name__)
            logger.setLevel(logging.INFO)
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

            if filename:
                file_handler = logging.FileHandler(filename)
                file_handler.setFormatter(formatter)
                logger.addHandler(file_handler)
            else:
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)
                logger.addHandler(console_handler)

            try:
                # Log function start
                logger.info(f"{func.__name__} started. Inputs: args={args}, kwargs={kwargs}")

                # Call the original function
                result = func(*args, **kwargs)

                # Log function success
                logger.info(f"{func.__name__} ok. Result: {result}")
                return result
            except Exception as e:
                # Log function error
                logger.error(f"{func.__name__} error: {type(e).__name__}. Inputs: args={args}, kwargs={kwargs}")
                raise

        return wrapper

    return decorator


@log(filename="mylog.txt")
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
        formatted_number = f"{number:016d}"
        yield f"{formatted_number[:4]} {formatted_number[4:8]} {formatted_number[8:12]} {formatted_number[12:]}"


@log()
def generate_transaction_descriptions(transaction_data: List[Dict[str, Any]]) -> List[str]:
    """
    Функция для генерации описаний транзакций на основе входных данных.

    :param transaction_data: Список словарей с данными о транзакциях.
    :return: Список строк с описаниями транзакций.
    """
    descriptions = []
    for transaction in transaction_data:
        if transaction["type"] == "payment":
            descriptions.append(f"Payment of {transaction['amount']} to {transaction['recipient']}")
        elif transaction["type"] == "refund":
            descriptions.append(f"Refund of {transaction['amount']} from {transaction['sender']}")
        else:
            descriptions.append("Unknown transaction type")
    return descriptions


@log(filename="mylog.txt")
def filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> List[int]:
    """
    Функция для фильтрации транзакций по валюте.

    :param transactions: Список словарей с данными о транзакциях.
    :param currency: Валюта для фильтрации.
    :return: Список ID транзакций, соответствующих указанной валюте.
    """
    filtered_ids = []
    for transaction in transactions:
        if transaction.get("currency") == currency:
            filtered_ids.append(transaction["id"])
    return filtered_ids


@log(filename="mylog.txt")
def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя только первые 4 и последние 4 цифры.
    Args:
        card_number: Номер банковской карты в виде строки.
    Returns:
        Маскированный номер карты.
    """
    if not isinstance(card_number, str) or len(card_number) < 16:
        raise ValueError("Неверный формат номера карты.")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


@log(filename="mylog.txt")
def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.
    Args:
        account_number: Номер банковского счета в виде строки.
    Returns:
        Маскированный номер счета.
    """
    if not isinstance(account_number, str) or len(account_number) < 4:
        raise ValueError("Неверный формат номера счета.")
    return f"**{account_number[-4:]}"


@log(filename="mylog.txt")
def filter_by_state(data: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """Фильтрует данные по состоянию."""
    if state not in {"EXECUTED", "CANCELED", "PENDING"}:
        raise ValueError(f"Invalid state: {state}")
    # Return a filtered list based on the 'state' key
    return [item for item in data if item.get("state") == state]


@log(filename="mylog.txt")
def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует данные по дате."""
    try:
        # Return a sorted copy of the input data
        return sorted(data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
    except KeyError:
        raise KeyError("Missing 'date' key in data")


@log(filename="mylog.txt")
def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя только первые 4 и последние 4 цифры.
    Args:
        card_number: Номер банковской карты в виде строки.
    Returns:
        Маскированный номер карты.
    """
    if not isinstance(card_number, str) or len(card_number) < 16:
        raise ValueError("Неверный формат номера карты.")
    return f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"


@log(filename="mylog.txt")
def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.
    Args:
        account_number: Номер банковского счета в виде строки.
    Returns:
        Маскированный номер счета.
    """
    print(f"Input: {account_number}, Type: {type(account_number)}, Length: {len(account_number)}")
    if not isinstance(account_number, str) or len(account_number) < 4:
        raise ValueError("Неверный формат номера счета.")
    return f"**{account_number[-4:]}"


@log(filename="mylog.txt")
def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета, основываясь на типе.
    Args:
        account_info: Строка, содержащая информацию о карте или счете.
    Returns:
        Строка с замаскированным номером карты или счета.
    """
    parts = account_info.split()
    if len(parts) < 2:
        return account_info
    card_type = parts[0].lower()
    number_part = ""
    for part in parts[1:]:
        if any(char.isdigit() for char in part):
            number_part = " ".join(parts[parts.index(part) :])
            break
    if not number_part:
        return account_info
    number = number_part.replace(" ", "")
    try:
        if card_type in ["visa", "mastercard", "maestro", "мир"]:
            return f"{parts[0]} {get_mask_card_number(number)}"
        elif card_type == "счет":
            return f"{parts[0]} {get_mask_account(number)}"
        else:
            return account_info
    except ValueError:
        return account_info


@log(filename="mylog.txt")
def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате ISO 8601 в формат "ДД.ММ.ГГГГ".
    Принимает форматы с или без времени и часового пояса.
    Args:
        date_str: Строка с датой в формате ISO 8601.
    Returns:
         Строка с датой в формате "ДД.ММ.ГГГГ".
    """
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if match:
        year, month, day = match.groups()
        return f"{day}.{month}.{year}"
    return date_str


if __name__ == "__main__":
    card = "Visa Classic 1234567890123456"
    print(mask_account_card(card))
