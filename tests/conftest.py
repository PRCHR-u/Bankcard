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
def account_masking_test_cases(
        request: pytest.FixtureRequest) -> tuple[str, str]:
    return tuple(request.param)
