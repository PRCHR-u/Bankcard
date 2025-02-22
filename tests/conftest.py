from typing import Any, Dict, List

import pytest


# Фикстура для тестовых данных
@pytest.fixture()
def test_data() -> List[Dict[str, Any]]:
    return [
        {"id": 414, "state": "EXECUTED", "date": "2019-08-26T10:50:58.294041"},
        {"id": 939, "state": "EXECUTED", "date": "2019-08-26T10:51:25.917491"},
        {"id": 594, "state": "CANCELED", "date": "2019-08-26T10:51:30.273718"},
        {"id": 615, "state": "CANCELED", "date": "2019-08-26T10:51:34.139194"},
    ]


# Фикстура для генерации тестовых данных для mask_account_card
@pytest.fixture(
    params=[
        ("Visa Classic 1234567890123456", None),
        ("MasterCard Standard 9876543210987654", None),
    ]
)
def account_test_cases(request: pytest.FixtureRequest) -> tuple[str, str]:
    return tuple(request.param)


# Фикстура для генерации тестовых данных для get_date
@pytest.fixture(
    params=[
        ("2023-09-15T12:34:56+03:00", None),
        ("2023-09-15", None),
    ]
)
def date_test_cases(request: pytest.FixtureRequest) -> tuple[str, str]:
    return tuple(request.param)


# Фикстура для валидного номера карты.
@pytest.fixture
def valid_card_number() -> list[str]:
    return ["1234567890123456"]


# Фикстура для другого валидного номера карты.
@pytest.fixture
def another_valid_card_number() -> list[str]:
    return ["9876543210987654"]


# Фикстура для валидного номера счета.
@pytest.fixture
def valid_account_number() -> list[str]:
    return ["1234567890"]


# Фикстура для другого валидного номера счета.
@pytest.fixture
def another_valid_account_number() -> list[str]:
    return ["0987654321"]


# Фикстура для невалидного номера.
@pytest.fixture
def invalid_number() -> list[str]:
    return ["123"]


# Фикстура для набора тестовых данных по карточкам
@pytest.fixture(
    params=[
        ("1234567890123456", "1234 56** **** 3456"),
        ("9876543210987654", "9876 54** **** 7654"),
    ]
)
def card_test_cases(request: pytest.FixtureRequest) -> tuple[str, str]:
    return tuple(request.param)


# Фикстура для набора тестовых данных по счетам
@pytest.fixture(
    params=[
        ("1234567890123456", "1234 56* ** 3456"),
        ("9876543210987654", "9876 54* ** 7654"),
    ]
)
def account_masking_test_cases(request: pytest.FixtureRequest) -> tuple[str, str]:
    return tuple(request.param)


@pytest.fixture
def transactions() -> List[Dict[str, Any]]:
    return [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
        {
            "id": 873106923,
            "state": "EXECUTED",
            "date": "2019-03-23T01:09:46.296404",
            "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод со счета на счет",
            "from": "Счет 44812258784861134719",
            "to": "Счет 74489636417521191160",
        },
        {
            "id": 895315941,
            "state": "EXECUTED",
            "date": "2018-08-19T04:27:37.904916",
            "operationAmount": {"amount": "56883.54", "currency": {"name": "USD", "code": "USD"}},
            "description": "Перевод с карты на карту",
            "from": "Visa Classic 6831982476737658",
            "to": "Visa Platinum 8990922113665229",
        },
        {
            "id": 594226727,
            "state": "CANCELED",
            "date": "2018-09-12T21:27:25.241689",
            "operationAmount": {"amount": "67314.70", "currency": {"name": "руб.", "code": "RUB"}},
            "description": "Перевод организации",
            "from": "Visa Platinum 1246377376343588",
            "to": "Счет 14211924144426031657",
        },
    ]
