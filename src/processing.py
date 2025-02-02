def filter_by_state(data, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        data: Список словарей.
        state: Значение ключа 'state' для фильтрации (по умолчанию 'EXECUTED').

    Returns:
        Новый список словарей, содержащий только те словари, у которых ключ 'state'
        соответствует указанному значению.
    """
    filtered_data = [data for data in data if data.get('state') == state]
    return filtered_data

if __name__ == '__main__':
    test_data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]

    executed_data = filter_by_state(test_data)
    print("Отфильтрованные данные (по умолчанию 'EXECUTED'):")
    for item in executed_data:
        print(item)

    pending_data = filter_by_state(test_data, state='PENDING')
    print("\nОтфильтрованные данные (по состоянию 'PENDING'):")
    for item in pending_data:
        print(item)

    failed_data = filter_by_state(test_data, state='FAILED')
    print("\nОтфильтрованные данные (по состоянию 'FAILED'):")
    for item in failed_data:
        print(item)


from datetime import datetime

def sort_by_date(data, reverse=True):
    """
    Сортирует список словарей по дате (ключ 'date').

    Args:
        data: Список словарей, содержащих ключ 'date' в формате строки (ISO 8601).
        reverse: Порядок сортировки (True - убывание, False - возрастание).

    Returns:
        Новый список, отсортированный по дате.
    """
    def date_key(item):
        date_str = item.get('date')
        if date_str:
            return datetime.fromisoformat(date_str)
        return datetime.min  # Если 'date' отсутствует, ставим в начало при сортировке по возрастанию, в конец при сортировке по убыванию

    sorted_data = sorted(data, key=date_key, reverse=reverse)
    return sorted_data

if __name__ == '__main__':
    test_data = [{'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}]


    sorted_desc_data = sort_by_date(test_data)
    print("Отсортировано по дате (убывание):")
    for item in sorted_desc_data:
        print(item)

    sorted_asc_data = sort_by_date(test_data, reverse=False)
    print("\nОтсортировано по дате (возрастание):")
    for item in sorted_asc_data:
        print(item)

