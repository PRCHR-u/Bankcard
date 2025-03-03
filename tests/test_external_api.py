import pytest
from src.external_api import convert_to_rub
from unittest.mock import patch, MagicMock
import requests

@pytest.fixture
def mock_response():
    mock = MagicMock()
    mock.json.return_value = {
        "rates": {
            "USD": 75.0,
            "EUR": 85.0
        }
    }
    return mock

def test_convert_to_rub_rub(mock_response):
    transaction = {
        "amount": 100,
        "currency": "RUB"
    }
    with patch('requests.get', return_value=mock_response):
        result = convert_to_rub(transaction)
    assert result == 100.0

def test_convert_to_rub_usd(mock_response):
    transaction = {
        "amount": 100,
        "currency": "USD"
    }
    with patch('requests.get', return_value=mock_response):
        result = convert_to_rub(transaction)
    assert result == 7500.0  # 100 USD * 75 RUB/USD

def test_convert_to_rub_eur(mock_response):
    transaction = {
        "amount": 100,
        "currency": "EUR"
    }
    with patch('requests.get', return_value=mock_response):
        result = convert_to_rub(transaction)
    assert result == 8500.0  # 100 EUR * 85 RUB/EUR

def test_convert_to_rub_invalid_currency(mock_response):
    transaction = {
        "amount": 100,
        "currency": "GBP"
    }
    with patch('requests.get', return_value=mock_response):
        result = convert_to_rub(transaction)
    assert result == 100.0  # No conversion, return original amount

def test_convert_to_rub_request_exception():
    transaction = {
        "amount": 100,
        "currency": "USD"
    }
    with patch('requests.get', side_effect=requests.RequestException):
        result = convert_to_rub(transaction)
    assert result == 100.0  # No conversion, return original amount

def test_convert_to_rub_key_error(mock_response):
    transaction = {
        "amount": 100,
        "currency": "USD"
    }
    mock_response.json.return_value = {}  # Invalid JSON response
    with patch('requests.get', return_value=mock_response):
        result = convert_to_rub(transaction)
    assert result == 100.0  # No conversion, return original amount

def test_convert_to_rub_value_error():
    transaction = {
        "amount": "invalid_amount",
        "currency": "USD"
    }
    with patch('requests.get', return_value=MagicMock(json=lambda: {"rates": {"USD": 75.0}})):
        result = convert_to_rub(transaction)
    assert result == 0.0  # Invalid amount, return 0.0
