import pytest
from src.processing import filter_by_state, sort_by_date
from tests.conftest import test_data


@pytest.mark.parametrize(
    ("state", "expected_ids"),
    [
        ("EXECUTED", [414, 939]),
        ("CANCELED", [594, 615]),
        ("PENDING", []),
    ],
)
def test_filter_by_state(test_data: list[dict[str]], state: str,
                         expected_ids: list[int]):
    filtered_data = filter_by_state(test_data.copy(), state=state)

    filtered_ids = [item["id"] for item in filtered_data]

    assert filtered_ids == expected_ids


def test_filter_by_state_empty_data():
    data = []

    filtered_d = filter_by_state(data.copy(), state="EXECUTED")

    assert filtered_d == []


@pytest.mark.parametrize(
    ("reverse", "expected_ids"),
    [
        (True, [414, 615, 594, 939]),
        (False, [939, 594, 615, 414]),
    ],
)
def test_sort_by_date(test_data: list[dict[str]], reverse: bool,
                      expected_ids):
    if reverse is None or expected_ids is None:
        pytest.skip("Invalid parametrization")

    sorted_data = sort_by_date(reverse=reverse)

    sorted_id = [item["id"] for item in sorted_data]

    assert sorted_id == expected_ids
