import pytest
from src.utils import load_transactions
from pathlib import Path
import json  # Добавляем импорт json

def test_load_transactions_valid_json():
    test_data = [
        {
            "id": 1,
            "date": "2023-09-15T12:34:56Z",
            "type": "payment",
            "amount": 100,
            "currency": "USD",
            "recipient": "John Doe"
        },
        {
            "id": 2,
            "date": "2023-09-16T12:34:56Z",
            "type": "refund",
            "amount": 50,
            "currency": "EUR",
            "sender": "Jane Smith"
        }
    ]
    test_file_path = Path("data/test_operations.json")
    test_file_path.write_text(json.dumps(test_data))

    result = load_transactions(str(test_file_path))
    assert result == test_data

    test_file_path.unlink()

def test_load_transactions_empty_file():
    test_file_path = Path("data/test_operations.json")
    test_file_path.touch()

    result = load_transactions(str(test_file_path))
    assert result == []

    test_file_path.unlink()

def test_load_transactions_invalid_json():
    test_file_path = Path("data/test_operations.json")
    test_file_path.write_text("{invalid_json}")

    result = load_transactions(str(test_file_path))
    assert result == []

    test_file_path.unlink()

def test_load_transactions_nonexistent_file():
    test_file_path = Path("data/nonexistent_operations.json")

    result = load_transactions(str(test_file_path))
    assert result == []
