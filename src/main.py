import json
import os
import sys
from datetime import datetime

# Добавляем родительскую директорию в sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logs.logger import setup_logger
from src.utils import read_json_file
from src.csv_excel import read_csv_file, read_excel_file
from src.filters import filter_by_description
from src.masks import get_mask_card_number, get_mask_account

# Инициализация логгера для модуля
logger = setup_logger("main")

def main():
    """
    Основная логика программы.
    """
    logger.info("Начало работы программы")
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    while True:
        try:
            choice = int(input("Пользователь: "))
            if choice in [1, 2, 3]:
                break
            else:
                print("Неверный пункт меню. Пожалуйста, выберите 1, 2 или 3.")
        except ValueError:
            print("Неверный ввод. Пожалуйста, введите число.")

    if choice == 1:
        file_path = "data/transactions.json"  # Замените на ваш файл
        transactions = read_json_file(file_path)
        print("Для обработки выбран JSON-файл.")
    elif choice == 2:
        file_path = "data/transactions.csv"  # Замените на ваш файл
        transactions = read_csv_file(file_path)
        print("Для обработки выбран CSV-файл.")
    elif choice == 3:
        file_path = "data/transactions_excel.xlsx"  # Замените на ваш файл
        transactions = read_excel_file(file_path)
        print("Для обработки выбран XLSX-файл.")

    if not transactions:
        print("Нет данных для обработки.")
        logger.warning("Нет данных для обработки.")
        return

    # Фильтрация по статусу
    available_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status = input(f"Введите статус, по которому необходимо выполнить фильтрацию. Доступные для фильтровки статусы: {', '.join(available_statuses)}: ").upper()
        if status in available_statuses:
            break
        else:
            print(f"Статус операции \"{status}\" недоступен.")

    transactions = [t for t in transactions if t.get("state") == status]
    print(f"Операции отфильтрованы по статусу \"{status}\"")

    # Сортировка по дате
    sort_by_date = input("Отсортировать операции по дате? Да/Нет: ").lower()
    if sort_by_date == "да":
        sort_order = input("Отсортировать по возрастанию или по убыванию? ").lower()
        if sort_order == "по возрастанию":
            transactions.sort(key=lambda x: datetime.strptime(x.get("date"), "%Y-%m-%dT%H:%M:%S.%f"))
        elif sort_order == "по убыванию":
            transactions.sort(key=lambda x: datetime.strptime(x.get("date"), "%Y-%m-%dT%H:%M:%S.%f"), reverse=True)
        else:
            print("Неверный порядок сортировки.")

    # Фильтрация по рублю
    filter_by_rub = input("Выводить только рублевые транзакции? Да/Нет: ").lower()
    if filter_by_rub == "да":
        transactions = [t for t in transactions if t.get("operationAmount", {}).get("currency", {}).get("name") == "RUB"]

    # Фильтрация по слову в описании
    filter_by_word = input("Отфильтровать список транзакций по определенному слову в описании? Да/Нет: ").lower()
    if filter_by_word == "да":
        search_word = input("Введите слово для поиска: ")
        transactions = filter_by_description(transactions, search_word)

    print("Распечатываю итоговый список транзакций...")
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        logger.info("Не найдено ни одной транзакции, подходящей под условия фильтрации")
    else:
        print(f"Всего банковских операций в выборке: {len(transactions)}")
        for i, transaction in enumerate(transactions):
            date = transaction.get("date")
            description = transaction.get("description")
            account = transaction.get("to")
            operation_amount = transaction.get("operationAmount")
            amount = operation_amount.get("amount")
            currency = operation_amount.get("currency", {}).get("name")
            if account:
                masked_account = get_mask_account(account)
                print(f"{datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')} {description}\nСчет {masked_account}\nСумма: {amount} {currency}\n")

            card = transaction.get("from")
            if card:
                masked_card = get_mask_card_number(card)
                print(f"{datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f').strftime('%d.%m.%Y')} {description}\n{masked_card}\nСумма: {amount} {currency}\n")

    logger.info("Завершение работы программы")

if __name__ == "__main__":
    main()
