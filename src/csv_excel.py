import csv
import os
import sys

import pandas as pd

# Добавляем родительскую директорию в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logs.logger import setup_logger

# Инициализация логгера для модуля
logger = setup_logger("csv_excel")


def read_csv_file(file_path: str) -> list:
    """
    Читает данные из CSV-файла и возвращает список словарей с транзакциями.
    """
    logger.info(f"Попытка чтения файла CSV {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = list(reader)
        logger.debug(f"Успешное чтение файла CSV {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Файл CSV {file_path} не найден.")
    except Exception as e:
        logger.error(f"Ошибка при чтении файла CSV {file_path}: {e}")
    return []

def read_excel_file(file_path: str) -> list:
    """
    Читает данные из XLSX-файла и возвращает список словарей с транзакциями.
    """
    logger.info(f"Попытка чтения файла Excel {file_path}")
    try:
        df = pd.read_excel(file_path)
        data = df.to_dict(orient='records')
        logger.debug(f"Успешное чтение файла Excel {file_path}")
        return data
    except FileNotFoundError:
        logger.error(f"Файл Excel {file_path} не найден.")
    except Exception as e:
        logger.error(f"Ошибка при чтении файла Excel {file_path}: {e}")
    return []

csv_file_path = "data/transactions.csv"
excel_file_path = "data/transactions_excel.xlsx"

# Чтение данных из файлов
csv_transactions = read_csv_file(csv_file_path)
excel_transactions = read_excel_file(excel_file_path)
