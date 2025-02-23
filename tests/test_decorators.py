import logging

import pytest

from src.decorators import (
    card_number_generator,
    filter_by_currency,
    generate_transaction_descriptions,
    get_date,
    get_mask_account,
    get_mask_card_number,
    log,
    mask_account_card,
)


# Renamed functions to avoid conflicts with pytest's test discovery
@log()
def func_no_args():
    return "No args"


@log()
def func_with_args(x: int, y: int) -> int:
    return x + y


@log()
def func_with_kwargs(x: int, y: int) -> int:
    return x * y


@log()
def func_with_exception() -> None:
    raise ValueError("Test exception")


# Tests
def test_log_decorator_console_output(caplog):
    caplog.set_level(logging.INFO)
    result = func_no_args()  # Updated reference to the renamed function
    assert result == "No args"
    assert "func_no_args started. Inputs: args=(), kwargs={}" in caplog.text
    assert "func_no_args ok. Result: No args" in caplog.text


def test_log_decorator_console_output_with_args(caplog):
    caplog.set_level(logging.INFO)
    result = func_with_args(3, 4)
    assert result == 7
    assert ("func_with_args started. "
            "Inputs: args=(3, 4), kwargs={}") in caplog.text
    assert "func_with_args ok. Result: 7" in caplog.text


def test_log_decorator_console_output_with_kwargs(caplog):
    caplog.set_level(logging.INFO)
    result = func_with_kwargs(x=3, y=4)
    assert result == 12
    expected = ("func_with_kwargs started. "
                "Inputs: args=(), kwargs={'x': 3, 'y': 4}")
    assert expected in caplog.text
    assert "func_with_kwargs ok. Result: 12" in caplog.text


def test_log_decorator_console_output_with_exception(caplog):
    caplog.set_level(logging.INFO)
    with pytest.raises(ValueError, match="Test exception"):
        func_with_exception()
    assert ("func_with_exception started. "
            "Inputs: args=(), kwargs={}") in caplog.text
    assert ("func_with_exception error: ValueError. "
            "Inputs: args=(), kwargs={}") in caplog.text


def test_log_decorator_file_output(tmp_path):
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def local_func_with_file_logging() -> str:
        return "File logging"

    local_func_with_file_logging()
    assert log_file.exists(), f"Log file {log_file} does not exist"
    with open(log_file, "r") as f:
        content = f.read()
    assert ("local_func_with_file_logging started. "
            "Inputs: args=(), kwargs={}") in content
    assert "local_func_with_file_logging ok. Result: File logging" in content


def test_log_decorator_with_multiple_exceptions(caplog):
    caplog.set_level(logging.INFO)

    @log()
    def sample_function_with_exception(exception_type):
        if exception_type == "ValueError":
            raise ValueError("Test ValueError")
        elif exception_type == "TypeError":
            raise TypeError("Test TypeError")

    # Test ValueError
    with pytest.raises(ValueError, match="Test ValueError"):
        sample_function_with_exception("ValueError")
    assert ("sample_function_with_exception error: ValueError. "
            "Inputs: args=('ValueError',), kwargs={}") in caplog.text

    # Test TypeError
    with pytest.raises(TypeError, match="Test TypeError"):
        sample_function_with_exception("TypeError")
    assert ("sample_function_with_exception error: "
            "TypeError. Inputs: args=('TypeError',), kwargs={}") in caplog.text


def test_log_decorator_with_no_args(caplog):
    caplog.set_level(logging.INFO)

    @log()
    def sample_function_no_args():
        return "No args"

    result = sample_function_no_args()
    assert result == "No args"
    assert ("sample_function_no_args started. "
            "Inputs: args=(), kwargs={}") in caplog.text
    assert "sample_function_no_args ok. Result: No args" in caplog.text


def test_log_decorator_with_complex_args(caplog):
    caplog.set_level(logging.INFO)

    @log()
    def sample_function_with_complex_args(x: list, y: dict):
        return x + list(y.keys())

    result = sample_function_with_complex_args([1, 2], {"a": 3, "b": 4})
    assert result == [1, 2, "a", "b"]
    expected_log = ("sample_function_with_complex_args started. "
                    "Inputs: args=([1, 2], {'a': 3, 'b': 4}), kwargs={}")
    assert expected_log in caplog.text
    assert ("sample_function_with_complex_args ok. "
            "Result: [1, 2, 'a', 'b']") in caplog.text


def test_log_decorator_file_output_with_args(tmp_path):
    log_file = tmp_path / "test_log.txt"

    @log(filename=str(log_file))
    def sample_function_with_args(x, y):
        return x + y

    result = sample_function_with_args(3, 4)
    assert result == 7
    assert log_file.exists()

    with open(log_file, "r") as f:
        content = f.read()
    assert ("sample_function_with_args started. "
            "Inputs: args=(3, 4), kwargs={}") in content
    assert "sample_function_with_args ok. Result: 7" in content


def test_log_decorator_with_edge_cases(caplog):
    caplog.set_level(logging.INFO)

    @log()
    def sample_function_with_edge_cases(x: int, y: int):
        return x + y

    # Test with large numbers
    result = sample_function_with_edge_cases(10**9, 10**9)
    assert result == 2 * 10**9
    assert ("sample_function_with_edge_cases started. "
            "Inputs: args=(1000000000, 1000000000), kwargs={}") in caplog.text
    assert ("sample_function_with_edge_cases ok. "
            "Result: 2000000000") in caplog.text

    # Test with zero values
    result = sample_function_with_edge_cases(0, 0)
    assert result == 0
    assert ("sample_function_with_edge_cases started. "
            "Inputs: args=(0, 0), kwargs={}") in caplog.text
    assert "sample_function_with_edge_cases ok. Result: 0" in caplog.text


def test_card_number_generator_invalid_start():
    with pytest.raises(ValueError, match="Start value must be at least 1"):
        list(card_number_generator(0, 1000))


def test_card_number_generator_invalid_stop():
    with pytest.raises(ValueError, match="Stop value "
                                         "must not exceed 9999999999999999"):
        list(card_number_generator(1, 10000000000000000))


def test_card_number_generator_invalid_range():
    with pytest.raises(ValueError, match="Start value "
                                         "must be less than or "
                                         "equal to stop value"):
        list(card_number_generator(1000, 100))


def test_card_number_generator_single_value():
    generator = card_number_generator(1, 1)
    result = list(generator)
    assert result == ["0000 0000 0000 0001"]


def test_card_number_generator_multiple_values():
    generator = card_number_generator(1, 3)
    result = list(generator)
    assert result == ["0000 0000 0000 0001",
                      "0000 0000 0000 0002",
                      "0000 0000 0000 0003"]


def test_card_number_generator_large_numbers():
    generator = card_number_generator(9999999999999997, 9999999999999999)
    result = list(generator)
    assert result == ["9999 9999 9999 9997",
                      "9999 9999 9999 9998",
                      "9999 9999 9999 9999"]


def test_card_number_generator_logging(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def wrapper(start, stop):
        return list(card_number_generator(start, stop))

    result = wrapper(1, 3)
    assert result == ["0000 0000 0000 0001",
                      "0000 0000 0000 0002",
                      "0000 0000 0000 0003"]

    # Проверяем содержимое файла логов
    assert log_file.exists()
    with open(log_file, "r") as f:
        content = f.read()
    assert "wrapper started. Inputs: args=(1, 3), kwargs={}" in content
    assert (
            ("wrapper ok. Result: "
             "['0000 0000 0000 0001', "
             "'0000 0000 0000 0002', "
             "'0000 0000 0000 0003']")
            in content
    )


def test_generate_transaction_descriptions_payment():
    transaction_data = [{"type": "payment",
                         "amount": 100, "recipient": "John Doe"}]
    result = generate_transaction_descriptions(transaction_data)
    assert result == ["Payment of 100 to John Doe"]


def test_generate_transaction_descriptions_refund():
    transaction_data = [{"type": "refund", "amount": 50,
                         "sender": "Jane Smith"}]
    result = generate_transaction_descriptions(transaction_data)
    assert result == ["Refund of 50 from Jane Smith"]


def test_generate_transaction_descriptions_unknown_type():
    transaction_data = [{"type": "unknown", "amount": 200}]
    result = generate_transaction_descriptions(transaction_data)
    assert result == ["Unknown transaction type"]


def test_generate_transaction_descriptions_empty_input():
    transaction_data = []
    result = generate_transaction_descriptions(transaction_data)
    assert result == []


def test_generate_transaction_descriptions_multiple_transactions():
    transaction_data = [
        {"type": "payment", "amount": 100, "recipient": "John Doe"},
        {"type": "refund", "amount": 50, "sender": "Jane Smith"},
        {"type": "unknown", "amount": 200},
    ]
    result = generate_transaction_descriptions(transaction_data)
    assert result == ["Payment of 100 to John Doe",
                      "Refund of 50 from Jane Smith",
                      "Unknown transaction type"]


def test_generate_transaction_descriptions_logging(caplog):
    caplog.set_level(logging.INFO)

    transaction_data = [{
        "type": "payment", "amount": 100, "recipient": "John Doe"
    }]
    result = generate_transaction_descriptions(transaction_data)
    assert result == ["Payment of 100 to John Doe"]

    # Проверяем логи
    assert (
        "generate_transaction_descriptions started. "
        "Inputs: args=([{'type': 'payment', 'amount': 100, "
        "'recipient': 'John Doe'}],),"
        " kwargs={}"
        in caplog.text
    )
    assert ("generate_transaction_descriptions ok. "
            "Result: ['Payment of 100 to John Doe']") in caplog.text


def test_filter_by_currency_valid_currency():
    transactions = [
        {"id": 1, "currency": "USD", "amount": 100},
        {"id": 2, "currency": "EUR", "amount": 200},
        {"id": 3, "currency": "USD", "amount": 150},
    ]
    result = filter_by_currency(transactions, "USD")
    assert result == [1, 3]


def test_filter_by_currency_no_matching_currency():
    transactions = [
        {"id": 1, "currency": "USD", "amount": 100},
        {"id": 2, "currency": "EUR", "amount": 200},
    ]
    result = filter_by_currency(transactions, "GBP")
    assert result == []


def test_filter_by_currency_empty_transactions():
    transactions = []
    result = filter_by_currency(transactions, "USD")
    assert result == []


def test_filter_by_currency_missing_currency_key():
    transactions = [
        {"id": 1, "amount": 100},
        {"id": 2, "currency": "USD", "amount": 200},
        {"id": 3, "amount": 150},
    ]
    result = filter_by_currency(transactions, "USD")
    assert result == [2]


def test_filter_by_currency_logging(tmp_path):
    log_file = tmp_path / "mylog.txt"

    @log(filename=str(log_file))
    def wrapper(transactions, currency):
        return filter_by_currency(transactions, currency)

    transactions = [
        {"id": 1, "currency": "USD", "amount": 100},
        {"id": 2, "currency": "EUR", "amount": 200},
        {"id": 3, "currency": "USD", "amount": 150},
    ]
    result = wrapper(transactions, "USD")
    assert result == [1, 3]

    assert log_file.exists()
    with open(log_file, "r") as f:
        content = f.read()
    assert (
        "wrapper started. Inputs: args=("
        "[{'id': 1, 'currency': 'USD', 'amount': 100}, "
        "{'id': 2, 'currency': 'EUR', 'amount': 200}, "
        "{'id': 3, 'currency': 'USD', 'amount': 150}], "
        "'USD'), kwargs={}"
        in content
    )
    assert "wrapper ok. Result: [1, 3]" in content


def test_get_mask_card_number_valid():
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"


def test_get_mask_card_number_invalid_length():
    with pytest.raises(ValueError, match="Неверный формат номера карты."):
        get_mask_card_number("12345")


def test_get_mask_card_number_non_string():
    with pytest.raises(ValueError, match="Неверный формат номера карты."):
        get_mask_card_number(1234567890123456)  # Pass an integer


def test_get_mask_account_valid():
    result = get_mask_account("1234567890123456")
    assert result == "**3456"


def test_get_mask_account_invalid_length():
    with pytest.raises(ValueError, match="Неверный формат номера счета."):
        get_mask_account("123")  # Length is less than 4


def test_get_mask_account_non_string():
    with pytest.raises(ValueError, match="Неверный формат номера счета."):
        get_mask_account([1, 2, 3, 4])  # Pass a list


def test_mask_account_card_valid_card():
    result = mask_account_card("Visa Classic 1234567890123456")
    assert result == "Visa 1234 56** **** 3456"


def test_mask_account_card_valid_account():
    result = mask_account_card("Счет 1234567890123456")
    assert result == "Счет **3456"


def test_mask_account_card_invalid_format():
    result = mask_account_card("Invalid 1234")
    assert result == "Invalid 1234"


def test_get_date_valid_iso_format():
    result = get_date("2023-09-15T12:34:56Z")
    assert result == "15.09.2023"


def test_get_date_valid_date_only():
    result = get_date("2023-09-15")
    assert result == "15.09.2023"


def test_get_date_invalid_format():
    result = get_date("invalid-date")
    assert result == "invalid-date"
