from src.services import filter_by_state


def test_filter_by_state() -> None:
    transactions = [
        {
            "Дата операции": "07.05.2024 10:12:16",
            "Дата платежа": "07.05.2024",
            "Номер карты": "nan",
            "Статус": "OK",
            "Сумма операции": -140.0,
            "Валюта операции": "RUB",
            "Сумма платежа": -140.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Переводы",
            "MCC": "nan",
            "Описание": "Богдан Л.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0.0,
            "Сумма операции с округлением": 140.0,
        },
        {
            "Дата операции": "05.05.2024 21:21:45",
            "Дата платежа": "05.05.2024",
            "Номер карты": "*1130",
            "Статус": "OK",
            "Сумма операции": 6000.0,
            "Валюта операции": "RUB",
            "Сумма платежа": 6000.0,
            "Валюта платежа": "RUB",
            "Кэшбэк": "nan",
            "Категория": "Переводы",
            "MCC": "nan",
            "Описание": "Марина М.",
            "Бонусы (включая кэшбэк)": 0,
            "Округление на инвесткопилку": 0.0,
            "Сумма операции с округлением": 6000.0,
        },
    ]
    assert filter_by_state(transactions) == [{'Дата операции': '07.05.2024 10:12:16', 'Дата платежа': '07.05.2024', 'Номер карты': 'nan', 'Статус': 'OK', 'Сумма операции': -140.0, 'Валюта операции': 'RUB', 'Сумма платежа': -140.0, 'Валюта платежа': 'RUB', 'Кэшбэк': 'nan', 'Категория': 'Переводы', 'MCC': 'nan', 'Описание': 'Богдан Л.', 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0.0, 'Сумма операции с округлением': 140.0}, {'Дата операции': '05.05.2024 21:21:45', 'Дата платежа': '05.05.2024', 'Номер карты': '*1130', 'Статус': 'OK', 'Сумма операции': 6000.0, 'Валюта операции': 'RUB', 'Сумма платежа': 6000.0, 'Валюта платежа': 'RUB', 'Кэшбэк': 'nan', 'Категория': 'Переводы', 'MCC': 'nan', 'Описание': 'Марина М.', 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0.0, 'Сумма операции с округлением': 6000.0}]