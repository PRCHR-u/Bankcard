from datetime import datetime


def filter_by_state(data, state) -> None:
    """Filters a list of dictionaries by the 'state' key."""
    allowed_states = ["EXECUTED", "CANCELED", "PENDING"]  # Define valid states
    if state not in allowed_states:
        raise ValueError(
            f"Invalid state: {state}." f"Allowed states are: {allowed_states}")

    filtered_data = [item for item in data if item.get("state") == state]
    return filtered_data


def sort_by_date(data, reverse=False) -> None:
    """Sorts a list of dictionaries by the 'date' key."""
    try:
        sorted_data = sorted(
            data, key=lambda x: datetime.fromisoformat(x["date"]),
            reverse=reverse)
    except KeyError:
        raise KeyError("Missing 'date' key in one" "or more data items")
    return sorted_data
