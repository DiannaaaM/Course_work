import json
import time
from pathlib import Path

import pandas as pd
import requests
import yfinance as yf

from src.utils import read_xls_file

reader = read_xls_file("../data/operations.xls")


def greeting(hour):
    if 5 < hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_number(reader):
    if reader is not None:
        for transaction in reader:
            return transaction["Номер карты"]
    else:
        return None


card_numbers = get_card_number(reader)


def total_sum_amount(reader, card_number):
    total = 0
    if card_number:
        for transaction in reader:
            total += transaction["Сумма операции"]
    return total


total_sum = total_sum_amount(reader, card_numbers)


def get_cashback(total_sum):
    return total_sum // 100


cashbacks = get_cashback(total_sum)


def top_transactions(reader):
    if reader is not None:

        def sort_by_sum(item):
            return item["Сумма операции"]

        reader.sort(key=sort_by_sum, reverse=True)

        result = []
        i = 0
        for transaction in reader:
            if i < 5:
                result.append(
                    {
                        "date": transaction["Дата операции"],
                        "amount": transaction["Сумма операции"],
                        "category": transaction["Категория"],
                        "description": transaction["Описание"],
                    }
                )
                i += 1
            else:
                break
        return result
    else:
        return None


top_transactions = top_transactions(reader)


def get_currency_rate(currency):
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": "RgcvuCoKJiBgqVod7PgrcSNPzdTt51jP"}, timeout=15)
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    return rate


def get_stock_currency(stock):
    ticker = yf.Ticker(stock)
    todays_data = pd.DataFrame(ticker.history(period="1d"))
    todays_data_dict = todays_data.to_dict(orient="records")
    return todays_data_dict[0]["High"]


def create_operations(read_xls_file):
    data = {"greeting": greeting(7), "cards": [], "top_transactions": [], "currency_rates": [], "stock_prices": []}
    if read_xls_file:
        for line in read_xls_file:
            card_number = card_numbers
            if card_number not in [card["last_digits"] for card in data["cards"]] and card_number is not None:
                data["cards"].append(
                    {"last_digits": card_number, "total_spent": round(total_sum, 2), "cashback": cashbacks}
                )
        data["top_transactions"].append(top_transactions)
        data["currency_rates"].append(
            (
                {"currency": "USD", "rate": round(get_currency_rate("USD"), 2)},
                {"currency": "EUR", "rate": round(get_currency_rate("EUR"), 2)},
            )
        )
        data["stock_prices"].append(
            [
                {"stock": "AAPL", "price": round(get_stock_currency("AAPL"), 2)},
                {"stock": "AMZN", "price": round(get_stock_currency("AMZN"), 2)},
                {"stock": "GOOGL", "price": round(get_stock_currency("GOOGL"), 2)},
                {"stock": "MSFT", "price": round(get_stock_currency("MSFT"), 2)},
                {"stock": "TSLA", "price": round(get_stock_currency("TSLA"), 2)},
            ]
        )
    return data


def write_data(create_operations):
    with open("../data/user_settings.json", "w", encoding="utf8") as f:
        json.dump(create_operations, f, ensure_ascii=False)


write_data(create_operations(read_xls_file("../data/operations.xls")))
