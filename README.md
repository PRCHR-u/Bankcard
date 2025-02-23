# Проект "Bankcard"

## Описание:

Проект "Bankcard" - это виджет банковских операций клиента на Python. 

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/PRCHR-u/Bankcard
```

2. Установите зависимости:
```
pip install -r requirements.txt
```

## Использование:

1. Откройте банковское приложение.
2. Зайдите в личный кабинет.
3. Откройте вкладку, содержащую последние операции по карте.

## Документация:

Вероятно этот раздел нужен, но я совсем не знаю, что сюда писать на данном этапе.

## Лицензия:

Проект не лицензирован

## Тестирование:

проект покрыт тестами pytest. Для их запуска выполните команду:
pytest

Тестируются функции get_mask_card_number, get_mask_account, mask_account_card, filter_by_state, get_date, sort_by_date

Тесты используют фикстуры из файла conftest.py

Каждый модуль имеет собственный файл тестирования. Все тесты параметризованы.

## Модули

### generators.py

Модуль generators.py содержит функции для генерации различных элементов, связанных с банковскими картами.

#### Функции

1. card_number_generator(start: int, stop: int) -> Generator[str, None, None]
Генератор для генерации номеров банковских карт в заданном диапазоне.
Параметры:
start (int): Начальное значение диапазона (минимум 1).
stop (int): Конечное значение диапазона (максимум 9999999999999999).
Возвращает:
Генератор строк в формате XXXX XXXX XXXX XXXX.

2. generate_transaction_descriptions(transaction_data: List[Dict[str, Any]]) -> List[str]
Функция для генерации описаний транзакций на основе входных данных.
Параметры:
transaction_data (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
Возвращает:
Список строк с описаниями транзакций.

3. filter_by_currency(transactions: List[Dict[str, Any]], currency: str) -> List[int]
Функция для фильтрации транзакций по валюте.
Параметры:
transactions (List[Dict[str, Any]]): Список словарей с данными о транзакциях.
currency (str): Валюта для фильтрации.
Возвращает:
Список ID транзакций, соответствующих указанной валюте.

#### Примеры использования

##### 1. Генерация номеров карт
``from src.generators import card_number_generator
for card_number in card_number_generator(1, 3):
    print(card_number)
Вывод:
0000 0000 0000 0001 
0000 0000 0000 0002
0000 0000 0000 0003``

##### 2. Генерация описаний транзакций
``from src.generators import generate_transaction_descriptions
transaction_data = [
    {"type": "payment", "amount": 100, "recipient": "John"},
    {"type": "refund", "amount": 50, "sender": "Alice"},
]
descriptions = generate_transaction_descriptions(transaction_data)
print(descriptions)
Вывод:
['Payment of 100 to John', 'Refund of 50 from Alice']``

##### 3. Фильтрация транзакций по валюте

``from src.generators import filter_by_currency
transactions = [
    {"id": 1, "currency": "USD", "amount": 100},
    {"id": 2, "currency": "RUB", "amount": 5000},
    {"id": 3, "currency": "USD", "amount": 200},
]
usd_transactions = filter_by_currency(transactions, "USD")
print(usd_transactions)
Вывод:
[1, 3]``

### decorators.py

Модуль decorators.py содержит декораторы для улучшения функциональности и логирования.

#### Декоратор log
Декоратор log автоматически логирует начало и конец выполнения функции, а также ее результаты или возникшие ошибки.

Параметры:

filename (Optional[str]): Имя файла для записи логов. Если None, логи выводятся в консоль.

Пример использования:
```from bankcard.decorators import log

@log(filename="mylog.txt")
def my_function(x, y):
    return x + y

my_function(1, 2)```