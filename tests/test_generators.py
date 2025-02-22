from typing import Any, Dict, List

import pytest

from src.generators import (card_number_generator,
                            filter_by_currency, transaction_descriptions)


@pytest.mark.parametrize(
    ("currency", "expected_ids"),
    [
        ("USD", [939719570, 142264268, 895315941]),
        ("RUB", [873106923, 594226727]),
        ("EUR", []),
    ],
)
def test_filter_by_currency(transactions: List[Dict[str, Any]],
                            currency: str, expected_ids: List[int]) -> None:
    """Тестирует генератор filter_by_currency с параметризацией."""
    usd_transactions = list(filter_by_currency(transactions, currency))
    assert [tx["id"] for tx in usd_transactions] == expected_ids


def test_filter_by_currency_empty_data() -> None:
    """Тестирует генератор filter_by_currency с пустыми данными."""
    data: List[Dict[str, Any]] = []
    usd_transactions = list(filter_by_currency(data, "USD"))
    assert usd_transactions == []


def test_filter_by_currency_missing_currency_key(transactions:
List[Dict[str, Any]]) -> None:
    """Тестирует обработку данных без ключа 'currency'."""
    data = [
        {
            "id": 999,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": 500.0},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]
    usd_transactions = list(filter_by_currency(data, "USD"))
    assert usd_transactions == []


@pytest.mark.parametrize(
    ("transaction_data", "expected_descriptions"),
    [
        (
            [
                {
                    "id": 999,
                    "state": "EXECUTED",
                    "date": "2019-08-26T10:50:58.294041",
                    "operationAmount": {"amount": 500.0, "currency":
                        {"name": "USD", "code": "USD"}},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                }
            ],
            ["Перевод организации"],
        ),
        ([], []),
        (
            [
                {
                    "id": 999,
                    "state": "EXECUTED",
                    "date": "2019-08-26T10:50:58.294041",
                    "operationAmount": {"amount": 500.0},
                    "description": "Перевод организации",
                    "from": "Счет 75106830613657916952",
                    "to": "Счет 11776614605963066702",
                }
            ],
            [],
        ),
    ],
)
def generate_transaction_descriptions(transaction_data):
    descriptions = []
    for transaction in transaction_data:
        if "type" not in transaction:
            descriptions.append("Invalid transaction: missing 'type'")
            continue

        if transaction["type"] == "payment":
            if "amount" not in transaction or "recipient" not in transaction:
                descriptions.append("Invalid payment transaction")
            else:
                descriptions.append(f"Payment of {transaction['amount']}"
                                    f"to {transaction['recipient']}")
        elif transaction["type"] == "refund":
            if "amount" not in transaction or "sender" not in transaction:
                descriptions.append("Invalid refund transaction")
            else:
                descriptions.append(f"Refund of {transaction['amount']} "
                                    f"from {transaction['sender']}")
        else:
            descriptions.append("Unknown transaction type")
    return descriptions


def test_transaction_descriptions_fxt(transactions: List[Dict[str, Any]]) -> None:
    """Тестирует генератор transaction_descriptions."""
    descriptions = list(transaction_descriptions(transactions))
    expected_descriptions = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert descriptions == expected_descriptions


def test_transaction_descriptions_empty_data() -> None:
    """Тестирует генератор transaction_descriptions с пустыми данными."""
    data: List[Dict[str, Any]] = []
    descriptions = list(transaction_descriptions(data))
    assert descriptions == []


def test_transaction_descriptions_missing_description_key(
        transactions: List[Dict[str, Any]]
) -> None:
    """Тестирует обработку данных без ключа '
    description' в генераторе transaction_descriptions."""
    data = [
        {
            "id": 999,
            "state": "EXECUTED",
            "date": "2019-08-26T10:50:58.294041",
            "operationAmount": {"amount": 500.0,
                                "currency": {"name": "USD", "code": "USD"}},
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        }
    ]
    descriptions = list(transaction_descriptions(data))
    assert descriptions == []


@pytest.mark.parametrize(
    ("start", "stop", "expected_numbers"),
    [
        (
            1,
            5,
            [
                "0000 0000 0000 0001",
                "0000 0000 0000 0002",
                "0000 0000 0000 0003",
                "0000 0000 0000 0004",
                "0000 0000 0000 0005",
            ],
        ),
        (1000, 1002, ["0000 0000 0000 1000",
                      "0000 0000 0000 1001", "0000 0000 0000 1002"]),
        (9999999999999998, 9999999999999999,
         ["9999 9999 9999 9998", "9999 9999 9999 9999"]),
    ],
)
def test_card_number_generator(start: int, stop: int,
                               expected_numbers: List[str]) -> None:
    """Тестирует генератор card_number_generator с параметризацией."""
    card_numbers = list(card_number_generator(start, stop))
    assert card_numbers == expected_numbers


@pytest.mark.timeout(5)  # Тест завершится через 5 секунд, если зависнет
def test_card_number_generator_invalid_range():
    """Тест для случая, когда start > stop."""
    start = 1000
    stop = 999  # Некорректный диапазон

    with pytest.raises(ValueError) as exc_info:
        list(card_number_generator(start, stop))

    assert str(exc_info.value) == ("Start value must be less than "
                                   "or equal to stop value")
