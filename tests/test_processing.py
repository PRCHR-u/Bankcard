from datetime import datetime
from typing import Any, Dict, List

import pytest

from src.processing import filter_by_state, sort_by_date


# Test filter_by_state function
@pytest.mark.parametrize(
    ("state", "expected_ids"),
    [
        ("EXECUTED", [414, 939]),
        ("CANCELED", [594, 615]),
        ("PENDING", []),
    ],
)
def test_filter_by_state(test_data: List[Dict[str, Any]],
                         state: str, expected_ids: List[int]) -> None:
    """Тестирует функцию filter_by_state."""
    filtered_data = filter_by_state(test_data.copy(), state=state) or []
    filtered_ids = [item["id"] for item in filtered_data]
    assert filtered_ids == expected_ids


def test_filter_by_state_empty_data() -> None:
    """Тестирует функцию filter_by_state с пустыми данными."""
    data: List[Dict[str, Any]] = []
    filtered_data = filter_by_state(data.copy(), state="EXECUTED")
    assert filtered_data == []


def test_filter_invalid_state(test_data: List[Dict[str, Any]]) -> None:
    """Тестирует обработку невалидных состояний в filter_by_state."""
    with pytest.raises(ValueError):
        filter_by_state(test_data.copy(), state="UNKNOWN")


# Test sort_by_date function
@pytest.mark.parametrize(
    ("reverse", "expected_ids", "expected_dates"),
    [
        (
            True,
            [615, 594, 939, 414],
            [
                datetime(2019, 8, 26, 10, 51, 34, 139194),
                datetime(2019, 8, 26, 10, 51, 30, 273718),
                datetime(2019, 8, 26, 10, 51, 25, 917491),
                datetime(2019, 8, 26, 10, 50, 58, 294041),
            ],
        ),
        (
            False,
            [414, 939, 594, 615],
            [
                datetime(2019, 8, 26, 10, 50, 58, 294041),
                datetime(2019, 8, 26, 10, 51, 25, 917491),
                datetime(2019, 8, 26, 10, 51, 30, 273718),
                datetime(2019, 8, 26, 10, 51, 34, 139194),
            ],
        ),
    ],
)
def test_sort_by_date(
    test_data: List[Dict[str, Any]], reverse: bool,
        expected_ids: List[int], expected_dates: List[datetime]
) -> None:
    """Тестирует функцию sort_by_date."""
    sorted_data = sort_by_date(test_data.copy(), reverse=reverse) or []
    sorted_ids = [item["id"] for item in sorted_data]
    sorted_dates = [datetime.fromisoformat(item["date"])
                    for item in sorted_data]
    assert sorted_ids == expected_ids
    assert sorted_dates == expected_dates


def test_sort_by_date_missing_dates() -> None:
    """Тестирует обработку данных без ключа 'date' в sort_by_date."""
    data = [{"id": 999}]  # Missing 'date' key
    with pytest.raises(KeyError):
        sort_by_date(data.copy())


def test_sort_by_date_empty_data() -> None:
    """Тестирует функцию sort_by_date с пустыми данными."""
    data: List[Dict[str, Any]] = []
    sorted_data = sort_by_date(data.copy()) or []  # Ensure it returns a list
    assert sorted_data == []
