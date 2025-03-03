import json
import os

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
