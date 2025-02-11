import pytest
from typing import List, Dict, Any

# Фикстура для тестовых данных
@pytest.fixture
def test_data() -> list[dict[str, str | int] | dict[str, str | int] | dict[str, str | int] | dict[str, str | int]]:
    return [
        {"id": 414, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

# Фикстура для генерации тестовых данных для mask_account_card
@pytest.fixture(params=[
    ("Visa Classic 1234567890123456", None),
    ("MasterCard Standard 9876543210987654", None),
])
def account_test_cases(request):
    return request.param

# Фикстура для генерации тестовых данных для get_date
@pytest.fixture(params=[
    ("2023-09-15T12:34:56+03:00", None),
    ("2023-09-15", None),
])
def date_test_cases(request):
    return request.param

#Фикстура для валидного номера карты.
@pytest.fixture
def valid_card_number() -> str:
    return ["1234567890123456"]

#Фикстура для другого валидного номера карты.
@pytest.fixture
def another_valid_card_number() -> str:
    return ["9876543210987654"]

#Фикстура для валидного номера счета.
@pytest.fixture
def valid_account_number() -> str:
    return ["1234567890"]

#Фикстура для другого валидного номера счета.
@pytest.fixture
def another_valid_account_number() -> str:
    return ["0987654321"]

#Фикстура для невалидного номера.
@pytest.fixture
def invalid_number() -> str:
    return ["123"]
