import datetime
import unittest
from unittest import TestCase

from pytest import mark, fixture

from src.views import greeting, get_card_number, total_sum_amount,get_cashback

@fixture()
def date_with_data():
    return [
  {
    'Дата операции': '31.05.2024 17:49:17',
    'Дата платежа': '31.05.2024',
    'Номер карты': '*1130',
    'Статус': 'OK',
    'Сумма операции': -5.0,
    'Валюта операции': 'RUB',
    'Сумма платежа': -5.0,
    'Валюта платежа': 'RUB',
    'Кэшбэк': None,
    'Категория': 'Супермаркеты',
    'MCC': 5411.0,
    'Описание': 'SPAR',
    'Бонусы (включая кэшбэк)': 0,
    'Округление на инвесткопилку': 45.0,
    'Сумма операции с округлением': 50.0
  },
  {
    'Дата операции': '31.05.2024 17:49:03',
    'Дата платежа': '31.05.2024',
    'Номер карты': '*1130',
    'Статус': 'OK',
    'Сумма операции': -365.49,
    'Валюта операции': 'RUB',
    'Сумма платежа': -365.49,
    'Валюта платежа': 'RUB',
    'Кэшбэк': 3.0,
    'Категория': 'Супермаркеты',
    'MCC': 5411.0,
    'Описание': 'SPAR',
    'Бонусы (включая кэшбэк)': 3,
    'Округление на инвесткопилку': 34.51,
    'Сумма операции с округлением': 400.0
  }]

@mark.parametrize(
    "hour, expected",
    [
        ("07.05.2023 08:00", "Доброе утро"),
        ("12.05.2023 13:00", "Добрый день"),
        ("20.05.2023 21:00", "Добрый вечер"),
        ("23.05.2023 00:00", "Доброй ночи"),
    ],
)
def test_greeting(hour: str, expected: str) -> None:
    assert greeting(hour) == expected

def test_get_card_number(date_with_data):
    assert get_card_number(date_with_data) == "*1130"
    assert get_card_number(None) is None

def test_total_sum_amount(date_with_data):
    assert total_sum_amount(date_with_data, "*1130") == 370

def test_get_cashback():
    assert get_cashback(370) == 3
    assert get_cashback(0) == 0
