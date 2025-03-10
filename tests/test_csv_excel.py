import pytest

from src.csv_excel import read_csv_file, read_excel_file


def test_read_csv_file():
    transactions = read_csv_file("data/transactions.csv")
    assert isinstance(transactions, list)


def test_read_excel_file():
    transactions = read_excel_file("data/transactions_excel.xlsx")
    assert isinstance(transactions, list)


def test_read_csv_file_not_found():
    transactions = read_csv_file("data/nonexistent.csv")
    assert transactions == []


def test_read_excel_file_not_found():
    transactions = read_excel_file("data/nonexistent.xlsx")
    assert transactions == []
