import json
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.main import main


# --------------------------
#  Вспомогательные функции
# --------------------------
def create_test_json_file(data, filename="data/test_transactions.json"):
    """Создает временный JSON файл для тестов."""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f)
    return filename


def create_test_csv_file(data,
                         filename="data/test_transactions.csv"):
    """Создает временный CSV файл для тестов."""
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        f.write("description,amount,state,operationAmount_currency_name\n")
        for row in data:
            op_amount = row.get(
                'operationAmount', {}).get('currency', {}).get('name', '')
            f.write(f"{row['description']},{row.get('amount', '')},"
                    f"{row['state']},{op_amount}\n")


def create_test_excel_file(data, filename="data/test_transactions.xlsx"):
    """Создает временный Excel файл для тестов."""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename


class TestMainFunction(unittest.TestCase):
    def setUp(self):
        self.mock_transactions = [
            {
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00.000",
                "description": "Payment for services",
                "to": "Счет 12345678901234567890",
                "operationAmount": {
                    "amount": "100.00",
                    "currency": {"name": "RUB"}
                }
            },
            {
                "state": "CANCELED",
                "date": "2023-02-01T15:30:00.000",
                "description": "Online purchase",
                "from": "Visa Classic 5469008999634848",
                "operationAmount": {
                    "amount": "50.00",
                    "currency": {"name": "USD"}
                }
            },
            {
                "state": "CANCELED",
                "date": "2023-02-01T15:30:00.000",
                "description": "Online purchase",
                "from": "Visa Classic 5469008999634848",
                "operationAmount": {
                    "amount": "50.00",
                    "currency": {"name": "USD"}
                }
            }
        ]

    def test_full_flow(self):
        """Тест полного потока работы программы."""
        input_values = [
            '1',             # выбор JSON
            'EXECUTED',      # статус
            'да',            # сортировать по дате
            'по возрастанию',
            'да',            # фильтровать по RUB
            'нет'            # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_json_file',
                           return_value=self.mock_transactions):
                    main()
                output = mock_stdout.getvalue()
                self.assertIn("Для обработки выбран JSON-файл.", output)
                self.assertIn("Payment for services", output)
                self.assertIn("Счет **7890\nСумма: 100.00 RUB\n", output)
                self.assertNotIn("Online purchase", output)

    def test_invalid_menu_choice(self):
        input_values = [
            '5',  # неверный выбор
            '2',  # корректный выбор
            'EXECUTED', 'нет', 'нет', 'нет'  # остальные обязательные ответы
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                main()
                output = mock_stdout.getvalue()
                self.assertIn("Неверный пункт меню", output)
                self.assertIn("Для обработки выбран CSV-файл", output)

    def test_empty_transactions(self):
        """Тест для проверки логирования
        предупреждения при отсутствии транзакций."""
        with patch('src.main.logger') as mock_logger:
            input_values = ['1']
            with patch('builtins.input', side_effect=input_values):
                with patch('src.main.read_json_file', return_value=[]):
                    main()
                    mock_logger.warning.assert_called_with(
                        "Нет данных для обработки."
                    )

    def test_date_sorting(self):
        input_values = [
            '1',  # выбор JSON
            'CANCELED',
            'да',  # сортировать по дате
            'по убыванию',  # порядок сортировки
            'нет',  # не фильтровать по RUB
            'нет'  # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_json_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("01.02.2023", output)
                    self.assertIn("Online purchase", output)

    def test_rub_filter(self):
        """Тест для проверки фильтрации по рублю."""
        input_values = [
            '1',             # выбор JSON
            'EXECUTED',      # статус
            'нет',           # не сортировать по дате
            'да',            # фильтровать по RUB
            'нет'            # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_json_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Для обработки выбран JSON-файл.", output)
                    self.assertIn("Payment for services", output)
                    self.assertIn("Счет **7890\nСумма: 100.00 RUB\n", output)
                    self.assertNotIn("Online purchase", output)

    def test_masked_account_output(self):
        """Тест для проверки маскированного счета в выводе."""
        input_values = [
            '1',             # выбор JSON
            'EXECUTED',      # статус
            'нет',           # не сортировать по дате
            'нет',           # не фильтровать по RUB
            'нет'            # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_json_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Для обработки выбран JSON-файл.", output)
                    self.assertIn("Счет **7890\nСумма: 100.00 RUB\n", output)

    def test_invalid_status_input(self):
        """Тест для проверки неправильного выбора статуса."""
        input_values = [
            '1',             # выбор JSON
            'INVALID',       # неверный статус
            'EXECUTED',      # правильный статус
            'нет',           # не сортировать по дате
            'нет',           # не фильтровать по RUB
            'нет'            # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_json_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Статус операции \"INVALID\" недоступен.",
                                  output)
                    self.assertIn("Для обработки выбран JSON-файл.", output)
                    self.assertIn("Payment for services", output)
                    self.assertIn("Счет **7890\nСумма: 100.00 RUB\n", output)

    def test_no_transactions(self):
        input_values = [
            '1',  # выбор JSON
            'PENDING',  # статус, которого нет в тестовых данных
            'нет', 'нет', 'нет'  # остальные параметры
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_json_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Не найдено ни одной транзакции", output)

    def test_invalid_sort_order(self):
        """Тест для обработки неверного порядка сортировки."""
        input_values = [
            '1',             # выбор JSON
            'EXECUTED',      # статус
            'да',            # сортировать по дате
            'invalid',       # неверный порядок сортировки
            'нет',           # не фильтровать по RUB
            'нет'            # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_json_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Неверный порядок сортировки.", output)

    def test_valid_csv_path(self):
        """Тест для проверки выбора файла CSV."""
        input_values = [
            '2',             # выбор CSV
            'EXECUTED',      # статус
            'нет',           # не сортировать по дате
            'нет',           # не фильтровать по RUB
            'нет'            # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_csv_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Для обработки выбран CSV-файл.", output)
                    self.assertIn("Payment for services", output)
                    self.assertIn("Счет **7890\nСумма: 100.00 RUB\n", output)

    def test_valid_xlsx_path(self):
        """Тест для проверки выбора файла XLSX."""
        input_values = [
            '3',             # выбор XLSX
            'EXECUTED',      # статус
            'нет',           # не сортировать по дате
            'нет',           # не фильтровать по RUB
            'нет'            # не фильтровать по описанию
        ]
        with patch('builtins.input', side_effect=input_values):
            with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
                with patch('src.main.read_excel_file',
                           return_value=self.mock_transactions):
                    main()
                    output = mock_stdout.getvalue()
                    self.assertIn("Для обработки выбран XLSX-файл.", output)
                    self.assertIn("Payment for services", output)
                    self.assertIn("Счет **7890\nСумма: 100.00 RUB\n", output)


if __name__ == '__main__':
    unittest.main()
