import pytest

from src.masks import get_mask_account, get_mask_card_number

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
    ("input_data", "expected_output"),
    card_tests,
)
def test_get_mask_card_number(input_data: str, expected_output: str) -> None:
    """Тестирует функцию get_mask_card_number."""
    result = get_mask_card_number(input_data)
    assert result == expected_output


@pytest.mark.parametrize(
    ("input_data", "expected_output"),
    account_tests,
)
def test_get_mask_account(input_data: str, expected_output: str) -> None:
    """Тестирует функцию get_mask_account."""
    result = get_mask_account(input_data)
    assert result == expected_output


# Тест на невалидные данные.
def test_invalid_inputs() -> None:
    with pytest.raises(ValueError):
        get_mask_card_number("123")
