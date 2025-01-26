def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя только первые 4 и последние 4 цифры.

    Args:
        card_number: Номер банковской карты в виде строки.

    Returns:
        Маскированный номер карты.
    """
    if not isinstance(card_number, str) or len(card_number) < 16:
        raise ValueError("Неверный формат номера карты.")
    return f"{card_number[:4]} {card_number[5:6]}** **** {card_number[-4:]}"


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.

    Args:
        account_number: Номер банковского счета в виде строки.

    Returns:
        Маскированный номер счета.
    """
    if not isinstance(account_number, str) or len(account_number) < 4:
        raise ValueError("Неверный формат номера счета.")
    return f"**{account_number[-4:]}"


if __name__ == "__main__":
    card = "1234567890123456"
    account = "12345678901234567890"
    print(get_mask_card_number(card))
    print(get_mask_account(account))
