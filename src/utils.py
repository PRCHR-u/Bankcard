import json
import os
import sys

# Добавляем родительскую директорию в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logs.logger import setup_logger

# Инициализация логгера для модуля
logger = setup_logger("utils")


def read_json_file(file_path: str):
    logger.info(f"Попытка чтения файла {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        logger.debug(f"Успешное чтение файла {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Файл {file_path} не найден.")
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")


def load_transactions(file_path: str) -> list:
    logger.info(f"Попытка загрузки транзакций из файла {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                logger.debug(f"Успешная загрузка "
                             f"транзакций из файла {file_path}")
                return data
            else:
                logger.warning(f"Файл {file_path} содержит не список.")
    except (FileNotFoundError, json.JSONDecodeError, TypeError) as e:
        logger.error(f"Ошибка при загрузке "
                     f"транзакций из файла {file_path}: {e}", exc_info=True)
    return []


if __name__ == "__main__":
    file_path = "data/operations.json"
    logger.info("Начало выполнения программы")

    try:
        transactions = load_transactions(file_path)
        if transactions:
            logger.info(f"Загружено {len(transactions)} транзакций.")
        else:
            logger.warning("Транзакции не загружены.")
    except Exception as e:
        logger.error(f"Неизвестная ошибка: {e}", exc_info=True)

    logger.info("Завершение выполнения программы")
