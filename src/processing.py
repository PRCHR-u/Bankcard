from datetime import datetime
from typing import Any, Dict, List


def filter_by_state(data: List[Dict[str, Any]], state: str) -> List[Dict[str, Any]]:
    """Фильтрует данные по состоянию."""
    if state not in {"EXECUTED", "CANCELED", "PENDING"}:
        raise ValueError(f"Invalid state: {state}")

    # Return a filtered list based on the 'state' key
    return [item for item in data if item.get("state") == state]


def sort_by_date(data: List[Dict[str, Any]], reverse: bool = True) -> List[Dict[str, Any]]:
    """Сортирует данные по дате."""
    try:
        # Return a sorted copy of the input data
        return sorted(data, key=lambda x: datetime.fromisoformat(x["date"]), reverse=reverse)
    except KeyError:
        raise KeyError("Missing 'date' key in data")
