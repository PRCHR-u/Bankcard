import re

from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(account_info: str) -> str:
    """
    Маскирует номер карты или счета, основываясь на типе.

    Args:
        account_info: Строка, содержащая информацию о карте или счете.

    Returns:
        Строка с замаскированным номером карты или счета.
    """
    parts = account_info.split()
    if len(parts) < 2:
        return account_info

    card_type = parts[0].lower()
    number_part = " ".join(parts[1:])
    number = number_part.replace(" ", "")
    try:
        if card_type in ["visa", "mastercard", "maestro", "мир"]:
            return f"{parts[0]} {get_mask_card_number(number)}"
        elif card_type == "счет":
            return f"{parts[0]} {get_mask_account(number)}"
        else:
            return account_info
    except ValueError:
        return account_info


def get_date(date_str: str) -> str:
    """
    Преобразует строку с датой в формате ISO 8601 в формат "ДД.ММ.ГГГГ".
    Принимает форматы с или без времени и часового пояса.

    Args:
        date_str: Строка с датой в формате ISO 8601.

    Returns:
         Строка с датой в формате "ДД.ММ.ГГГГ".
    """
    match = re.match(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if match:
        year, month, day = match.groups()
        return f"{day}.{month}.{year}"
    return date_str
