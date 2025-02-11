import pytest

from src.masks import get_mask_account, get_mask_card_number


@pytest.mark.parametrize("input_data, expected_output")
def test_get_mask_card_number(input_data: str, expected_output: str):
    assert get_mask_card_number(input_data) == expected_output


@pytest.mark.parametrize("input_data, expected_output")
def test_get_mask_account(input_data: str, expected_output: str):
    assert get_mask_account(input_data) == expected_output


# Тест на невалидные данные
@pytest.mark.parametrize("invalid_input")
def test_invalid_input(invalid_input: str):
    with pytest.raises(ValueError):
        get_mask_card_number(invalid_input)

    with pytest.raises(ValueError):
        get_mask_account(invalid_input)

def test_get_mask_card_number(
    valid_card_number: str, another_valid_card_number: str, invalid_number: str
) -> None:
    """Тестирует функцию get_mask_card_number с использованием фикстур."""
    assert get_mask_card_number(valid_card_number) == "1234 56** **** 3456"
    assert get_mask_card_number(another_valid_card_number) == "9876 54** **** 7654"

    with pytest.raises(ValueError):
        get_mask_card_number(invalid_number)


def test_get_mask_account(
    valid_account_number: str, another_valid_account_number: str, invalid_number: str
) -> None:
    """Тестирует функцию get_mask_account с использованием фикстур."""
    assert get_mask_account(valid_account_number) == "**7890"
    assert get_mask_account(another_valid_account_number) == "**4321"

    with pytest.raises(ValueError):
        get_mask_account(invalid_number)
