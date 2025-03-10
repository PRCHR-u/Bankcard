import pytest
from src.filters import filter_by_description, categorize_transactions


def test_filter_by_description_empty_list():
    """Тест для пуcтого списка транзакций."""
    transactions = []
    search_string = "test"
    result = filter_by_description(transactions, search_string)
    assert result == []


def test_filter_by_description_no_match():
    """Тест для случая, когда нет совпадений."""
    transactions = [{"description": "Transaction 1"}, {"description": "Transaction 2"}]
    search_string = "test"
    result = filter_by_description(transactions, search_string)
    assert result == []


def test_filter_by_description_single_match():
    """Тест для случая, когда одно совпадение."""
    transactions = [{"description": "Transaction test"}, {"description": "Transaction 2"}]
    search_string = "test"
    result = filter_by_description(transactions, search_string)
    assert len(result) == 1
    assert result[0]["description"] == "Transaction test"


def test_filter_by_description_multiple_matches():
    """Тест для случая, когда несколько совпадений."""
    transactions = [{"description": "Transaction test"}, {"description": "test Transaction"}, {"description": "Transaction 2"}]
    search_string = "test"
    result = filter_by_description(transactions, search_string)
    assert len(result) == 2
    assert result[0]["description"] == "Transaction test"
    assert result[1]["description"] == "test Transaction"


def test_filter_by_description_case_insensitive():
    """Тест на нечувствительность к регистру."""
    transactions = [{"description": "Transaction Test"}, {"description": "Transaction 2"}]
    search_string = "test"
    result = filter_by_description(transactions, search_string)
    assert len(result) == 1
    assert result[0]["description"] == "Transaction Test"


def test_filter_by_description_empty_search_string():
    """Тест для пустой строки поиска."""
    transactions = [{"description": "Transaction 1"}, {"description": "Transaction 2"}]
    search_string = ""
    result = filter_by_description(transactions, search_string)
    assert len(result) == 2


def test_categorize_transactions_empty_list():
    """Тест для пустого списка транзакций."""
    transactions = []
    categories = {}
    result = categorize_transactions(transactions, categories)
    assert result == {}


def test_categorize_transactions_single_category():
    """Тест для одной категории."""
    transactions = [{"description": "Category 1"}, {"description": "Category 1"}]
    categories = {}
    expected = {"Category 1": 2}
    result = categorize_transactions(transactions, categories)
    assert result == expected


def test_categorize_transactions_multiple_categories():
    """Тест для нескольких категорий."""
    transactions = [{"description": "Category 1"}, {"description": "Category 2"}, {"description": "Category 1"}]
    categories = {}
    expected = {"Category 1": 2, "Category 2": 1}
    result = categorize_transactions(transactions, categories)
    assert result == expected

def test_categorize_transactions_existing_categories():
    """Тест для случая, когда категории уже существуют в словаре."""
    transactions = [{"description": "Category 1"}, {"description": "Category 2"}, {"description": "Category 1"}]
    categories = {"Category 3": 5}
    expected = {"Category 3": 5, "Category 1": 2, "Category 2": 1}
    result = categorize_transactions(transactions, categories)
    assert result == expected


def test_categorize_transactions_missing_description():
    """Тест для транзакций без описания."""
    transactions = [{}, {"description": "Category 1"}]
    categories = {}
    expected = {"Unknown": 1, "Category 1": 1}
    result = categorize_transactions(transactions, categories)
    assert result == expected
