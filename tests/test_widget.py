import pytest
from src.widget import mask_account_card, get_date


# Параметризация для mask_account_card
@pytest.mark.parametrize("input_data, expected_output", [
    ("Visa Classic 1234567890123456", "Visa 1234 56** **** 3456"),
    ("MasterCard Standard 9876543210987654", "MasterCard 9876 54** **** 7654"),
    ("Счет 40817810999910000001", "Счет **0001"),
    ("UnknownType 1234567890123456", "UnknownType 1234567890123456"),
    ("Visa Electron 1111", "Visa Electron 1111")
])
def test_mask_account_card(input_data, expected_output):
    """
    Тестирует функцию mask_account_card.

     Проверяет корректность маскировки номеров карт и счетов.
     """

    result = mask_account_card(input_data)

    assert result == expected_output, f"Ошибка при обработке {input_data}"


# Параметризация для get_date
@pytest.mark.parametrize("input_data, expected_output", [
    ("2023-09-15T12:34:56+03:00", "15.09.2023"),
    ("2023-09-15", "15.09.2023"),
    ("2023-09-15T12:34:56Z", "15.09.2023"),
    ("invalid-date", "invalid-date")
])
def test_get_date(input_data, expected_output):
    """
     Тестирует функцию get_date.

     Проверяет корректность преобразования даты из формата ISO
     в формат 'ДД.ММ.ГГГГ'.
     """

    # Получаем входные данные из фикстуры

    result = get_date(input_data)

    assert result == expected_output, f"Ошибка при обработке даты {input_data}"
