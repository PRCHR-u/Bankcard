import pytest

from src.masks import get_mask_account, get_mask_card_number


def test_get_mask_card_number() -> None:
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("9876543210987654") == "9876 54** **** 7654"

    with pytest.raises(ValueError):
        get_mask_card_number("123") is None
    with pytest.raises(ValueError):
        get_mask_card_number(str(123))


def test_get_mask_account() -> None:
    assert get_mask_account("1234567890") == "**7890"
    assert get_mask_account("0987654321") == "**4321"

    with pytest.raises(ValueError):
        get_mask_account("123") is None
    with pytest.raises(ValueError):
        get_mask_account(str(123))
