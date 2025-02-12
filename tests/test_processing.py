import pytest
from src.processing import filter_by_state, sort_by_date
from tests.conftest import test_data
from datetime import datetime

@pytest.mark.parametrize(
    ("state", "expected_ids"),
    [
        ("EXECUTED", [414, 939]),
        ("CANCELED", [594, 615]),
        ("PENDING", []),
    ],
)
def test_filter_by_state(test_data, state, expected_ids):
    filtered_data = filter_by_state(test_data.copy(), state=state)
    filtered_ids = [item["id"] for item in filtered_data]
    assert filtered_ids == expected_ids


def test_filter_by_state_empty_data():
    data = []
    filtered_d = filter_by_state(data.copy(), state="EXECUTED")
    assert filtered_d == []


def test_filter_invalid_state(test_data):
    with pytest.raises(ValueError):
        filter_by_state(test_data.copy(), state="UNKNOWN")


@pytest.mark.parametrize(
    ("reverse", "expected_ids", "expected_dates"),
    [
        (True, [615, 594, 939, 414], [datetime(2019, 8, 26, 10, 51, 34, 139194), datetime(2019, 8, 26, 10, 51, 30, 273718), datetime(2019, 8, 26, 10, 51, 25, 917491), datetime(2019, 8, 26, 10, 50, 58, 294041)]),
        (False, [414, 939, 594, 615], [datetime(2019, 8, 26, 10, 50, 58, 294041), datetime(2019, 8, 26, 10, 51, 25, 917491), datetime(2019, 8, 26, 10, 51, 30, 273718), datetime(2019, 8, 26, 10, 51, 34, 139194)])
    ],
)
def test_sort_by_date(test_data, reverse, expected_ids, expected_dates):
    sorted_data = sort_by_date(test_data.copy(), reverse=reverse)
    sorted_ids = [item["id"] for item in sorted_data]
    sorted_dates = [datetime.fromisoformat(item['date']) for item in sorted_data]
    assert sorted_ids == expected_ids
    assert sorted_dates == expected_dates


def test_sort_by_date_missing_dates():
    data = [{"id": 999}]  # Missing 'date' key
    with pytest.raises(KeyError):
        sort_by_date(data.copy())


def test_sort_by_date_empty_data():
    data = []
    sorted_d = sort_by_date(data.copy())
    assert sorted_d == []

