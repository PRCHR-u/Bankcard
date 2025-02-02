from src.widget import mask_account_card, get_date


def test_mask_account_card_mastercard():
    assert (mask_account_card("Mastercard 9876543210987654"), "Mastercard 9876 54** **** 7654")

def test_mask_account_card_maestro():
    assert (mask_account_card("Maestro 1234567890123456"), "Maestro 1234 56** **** 3456")

def test_mask_account_card_account():
    assert (mask_account_card("Visa Gold 12345678901234567890"), "Visa Gold **34567890** ****7890")

def test_mask_account_card_spaces_in_number():
    assert (mask_account_card("Visa 1234 5678 9012 3456"), "Visa 1234 56** **** 3456")

def test_get_date_with_time():
    assert (get_date("2023-10-26T10:30:00"), "26.10.2023")

def test_get_date_without_time():
    assert (get_date("2023-11-15"), "15.11.2023")

def test_get_date_invalid_format():
        assert (get_date("26/10/2023"), "26/10/2023")

