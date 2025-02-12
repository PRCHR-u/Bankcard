import pytest

from src.masks import get_mask_account, get_mask_card_number
from tests.conftest import invalid_number

# Определите наборы тестовых данных
card_tests = [
    ("1234567890123456", "1234 56** **** 3456"),
    ("9876543210987654", "9876 54** **** 7654"),
]

account_tests = [
    ("1234567890", "**7890"),
    ("0987654321", "**4321"),
]

invalid_nums = ["123"]

@pytest.mark.parametrize(
    (
            "input_data",
            "expected_output",
    ),
    card_tests + account_tests,
)
def test_get_masks(input_data: str,
                   expected_output: str):
    if len(input_data) > 10:
        result = get_mask_card_number(input_data)
    else:
        result = get_mask_account(input_data)

    assert result == expected_output


# Тест на невалидные данные
@pytest.mark.parametrize("invalid_input",
                         invalid_nums)
def test_invalid_inputs(invalid_input: str, invalid_number):
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_number)
