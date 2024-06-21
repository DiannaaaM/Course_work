import json
from typing import Any
from unittest import mock
from unittest.mock import patch

from pytest import fixture, mark

from src.utils import read_files
from src.views import get_card_number, get_cashback, get_currency_rate, get_stock_currency, greeting, total_sum_amount


@fixture()
def date_with_data() -> Any:
    return read_files("data/operations.xls")


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


def test_get_card_number(date_with_data: Any) -> None:
    assert get_card_number(date_with_data) == "*1130"
    assert get_card_number(None) is None


def test_total_sum_amount(date_with_data: Any) -> None:
    assert total_sum_amount(date_with_data, "*1130") == 2552


def test_get_cashback() -> None:
    assert get_cashback(370) == 3
    assert get_cashback(0) == 0


@patch("requests.get")
def test_get_currency_rate(mock_get: Any) -> None:
    mock_response = {"rates": {"RUB": 75.0}}
    mock_get.return_value.text = json.dumps(mock_response)
    transaction = {"amount": 100, "currency": "USD"}
    assert get_currency_rate(transaction) == 75.0


def test_get_stock_currency() -> None:
    mock_todays_data = mock.Mock()
    mock_todays_data_dict = [{"High": 100.0}]
    mock_todays_data.to_dict.return_value = mock_todays_data_dict

    with mock.patch("src.views.yf", autospec=True) as mock_yf:
        mock_ticker = mock.Mock()
        mock_yf.Ticker.return_value = mock_ticker
        mock_ticker.history.return_value = mock_todays_data

        result = get_stock_currency("AAPL")

        assert result == 0.0
        mock_yf.Ticker.assert_called_once_with("AAPL")
