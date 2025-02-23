import pytest
from src.decorators import log
import logging
import os


# Пример функций для тестирования декоратора
@log()
def test_function_no_args():
    return "No args"


@log()
def test_function_with_args(x: int, y: int) -> int:
    return x + y


@log()
def test_function_with_kwargs(x: int, y: int) -> int:
    return x * y


@log()
def test_function_with_exception() -> None:
    raise ValueError("Test exception")


@log(filename="test_log.txt")
def test_function_with_file_logging() -> str:
    return "File logging"


# Фикстура для перехвата логов
@pytest.fixture
def caplog(request, caplog):
    caplog.set_level(logging.INFO)
    yield caplog


# Тестирование вывода в консоль
def test_log_decorator_console_output(caplog):
    test_function_no_args()
    assert "test_function_no_args started. Inputs: args=(), kwargs={}" in caplog.text
    assert "test_function_no_args ok. Result: No args" in caplog.text


def test_log_decorator_console_output_with_args(caplog):
    result = test_function_with_args(3, 4)
    assert result == 7
    assert "test_function_with_args started. Inputs: args=(3, 4), kwargs={}" in caplog.text
    assert "test_function_with_args ok. Result: 7" in caplog.text


def test_log_decorator_console_output_with_kwargs(caplog):
    result = test_function_with_kwargs(x=3, y=4)
    assert result == 12
    assert "test_function_with_kwargs started. Inputs: args=(), kwargs={'x': 3, 'y': 4}" in caplog.text
    assert "test_function_with_kwargs ok. Result: 12" in caplog.text


def test_log_decorator_console_output_with_exception(caplog):
    with pytest.raises(ValueError) as exc_info:
        test_function_with_exception()
    assert "test_function_with_exception started. Inputs: args=(), kwargs={}" in caplog.text
    assert "test_function_with_exception error: ValueError. Inputs: args=(), kwargs={}" in caplog.text


# Тестирование записи в файл
def test_log_decorator_file_output(tmp_path):
    log_file = tmp_path / "test_log.txt"
    test_function_with_file_logging()
    assert log_file.exists(), f"Log file {log_file} does not exist"
    with open(log_file, "r") as f:
        content = f.read()
    assert "test_function_with_file_logging started. Inputs: args=(), kwargs={}" in content
    assert "test_function_with_file_logging ok. Result: File logging" in content


# Тестирование записи в файл с исключением
def test_log_decorator_file_output_with_exception(tmp_path):
    log_file = tmp_path / "test_log_exception.txt"

    @log(filename=str(log_file))
    def test_function_with_exception_in_file():
        raise ValueError("Test exception in file")

    with pytest.raises(ValueError) as exc_info:
        test_function_with_exception_in_file()

    assert log_file.exists(), f"Log file {log_file} does not exist"
    with open(log_file, "r") as f:
        content = f.read()
    assert "test_function_with_exception_in_file started. Inputs: args=(), kwargs={}" in content
    assert "test_function_with_exception_in_file error: ValueError. Inputs: args=(), kwargs={}" in content
