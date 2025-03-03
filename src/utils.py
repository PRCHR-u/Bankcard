import json
from logs.logger import setup_logger


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
    """
    Читает данные из JSON-файла и возвращает список словарей с транзакциями.
    Если файл пустой, содержит не список или не найден, возвращает пустой список.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError, TypeError):
        pass
    return []
