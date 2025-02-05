import pytest
from black import datetime

from src.processing import filter_by_state, sort_by_date
from typing import List, Dict, Any


@pytest.fixture
def sample_data() -> List[Dict[str, Any]]:
    """
    Фикстура для предоставления тестовых данных.
    """
    return [
        {"id": 414, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 594, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

@pytest.mark.parametrize(


def test_filter_by_state(sample_data: List[Dict[str, Any]]):
    """
    Тест: фильтрация по умолчанию ("EXECUTED").
    """
    result = filter_by_state(sample_data)
    assert len(result) == 2
    for item in result:
        assert item["state"] == "EXECUTED"


def test_filter_by_state_pending(sample_data: List[Dict[str, Any]]):
    """
    Тест: фильтрация по "PENDING".
    """
    result = filter_by_state(sample_data, state="PENDING")
    assert len(result) == 1
    assert result[0]["state"] == "PENDING"


def test_filter_by_state_failed(sample_data: List[Dict[str, Any]]):
    """
    Тест: фильтрация по "FAILED".
    """
    result = filter_by_state(sample_data, state="FAILED")
    assert len(result) == 1
    assert result[0]["state"] == "FAILED"


@pytest.fixture
def date_key() -> List[Dict[str, Any]]:
    """
    Фикстура для предоставления тестовых данных.
    """
    return [
        {"id": 412, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 937, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 592, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]

@pytest.mark.parametrize(
    "reverse, expected_ids",
                         [
        (False, [937, 592, 615, 412]),  # Ascending
        (True, [412, 615, 592, 937]),   # Descending
    ],
)

def test_sort_by_date_ascending(date_key_fixture: List[Dict[str, Any]]):
    """Тест: Сортировка по дате в порядке возрастания."""
    data = date_key_fixture
    expected_data = [
        {"id": 937, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 592, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 615, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 412, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    ]
    assert sort_by_date(data) == expected_data

def test_sort_by_date_descending(date_key_fixture: List[Dict[str, Any]]):
    """Тест: Сортировка по дате в порядке убывания."""
    data = date_key_fixture
    expected_data = [
        {"id": 412, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 592, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 937, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    assert sort_by_date(data, reverse=True) == expected_data


def test_same_dates(date_key_fixture: List[Dict[str, Any]]):
    """Тест: Корректность сортировки при одинаковых датах (сохранение исходного порядка)."""
    data = [
        {"id": 1, "date": "2023-10-26"},
        {"id": 2, "date": "2023-10-26"},
        {"id": 3, "date": "2023-10-26"}
    ]
    expected_data = data  # Исходный порядок должен сохраниться.
    assert sort_by_date(data) == expected_data


def test_different_date_formats():
    """Тест: Работа функции с разными форматами дат."""
    data = [
        {"id": 1, "date": "2023-10-27T10:00:00"},
        {"id": 2, "date": "2023-10-25"},
        {"id": 3, "date": "2023-10-26T12:30:00.500"}
    ]
    expected_data = [
        {"id": 2, "date": "2023-10-25"},
        {"id": 3, "date": "2023-10-26T12:30:00.500"},
        {"id": 1, "date": "2023-10-27T10:00:00"}
    ]
    assert sort_by_date(data) == expected_data


def test_invalid_date_format():
    """Тест: Функция должна корректно обрабатывать некорректные форматы дат (помещать их в конец)."""
    data = [
        {"id": 1, "date": "2023-10-27"},
        {"id": 2, "date": "invalid-date"},
        {"id": 3, "date": "2023-10-26"}
    ]
    expected_data = [
        {"id": 3, "date": "2023-10-26"},
        {"id": 1, "date": "2023-10-27"},
        {"id": 2, "date": "invalid-date"}  # Невалидная дата в конце
    ]
    assert sort_by_date(data) == expected_data


def test_missing_date_key():
    """Тест: Функция должна корректно обрабатывать отсутствие ключа с датой."""
    data = [
        {"id": 1, "date": "2023-10-27"},
        {"id": 2},
        {"id": 3, "date": "2023-10-26"}
    ]
    expected_data = [
        {"id": 3, "date": "2023-10-26"},
        {"id": 1, "date": "2023-10-27"},
        {"id": 2}  # Отсутствующий ключ в конце
    ]
    assert sort_by_date(data) == expected_data