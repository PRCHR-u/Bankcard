import logging
import os
import sys

# Добавляем родительскую директорию в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logs.logger import setup_logger

# Инициализация логгера для модуля
logger = setup_logger("masks")


def get_mask_card_number(card_number: str) -> str:
    """
    Маскирует номер карты, оставляя только первые 4 и последние 4 цифры.

    Args:
        card_number: Номер банковской карты в виде строки.

    Returns:
        Маскированный номер карты.
    """
    logger.info("Начало маскировки номера карты")
    try:
        if not isinstance(card_number, str) or len(card_number) < 16:
            raise ValueError("Неверный формат номера карты.")
        masked_card = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
        logger.debug(f"Маскированный номер карты: {masked_card}")
        return masked_card
    except Exception as e:
        logger.error(f"Ошибка при маскировке номера карты: {e}")
        raise


def get_mask_account(account_number: str) -> str:
    """
    Маскирует номер счета, оставляя видимыми только последние 4 цифры.

    Args:
        account_number: Номер банковского счета в виде строки.

    Returns:
        Маскированный номер счета.
    """
    logger.info("Начало маскировки номера счета")
    try:
        if not isinstance(account_number, str) or len(account_number) < 4:
            raise ValueError("Неверный формат номера счета.")
        masked_account = f"**{account_number[-4:]}"
        logger.debug(f"Маскированный номер счета: {masked_account}")
        return masked_account
    except Exception as e:
        logger.error(f"Ошибка при маскировке номера счета: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    logger.info("Начало выполнения программы")

    card = "1234567890123456"
    account = "12345678901234567890"

    try:
        print(get_mask_card_number(card))
        print(get_mask_account(account))
    except ValueError as ve:
        logger.error(f"Завершение программы с ошибкой: {ve}")
    except Exception as e:
        logger.critical(f"Неизвестная ошибка: {e}")

    logger.info("Завершение выполнения программы")
