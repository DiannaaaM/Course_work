import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
import yfinance as yf
from dotenv import load_dotenv

from src.utils import read_files, setup_logging, write_data

load_dotenv()
api_key = os.getenv("API_KEY")
logger = setup_logging()
reader_operations = read_files("../data/operations.xls")


def greeting(hour: Any) -> str:
    """
    Возвращает приветственное сообщение в зависимости от времени суток.
    """
    if hour is None:
        hour = datetime.now()
    else:
        hour = datetime.strptime(hour, "%d.%m.%Y %H:%M")
    hour = hour.hour
    if 5 < hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def get_card_number(reader: Any) -> Any:
    """
    Возвращает номер карты пользователя.
    """
    if reader is not None:
        for transaction in reader:
            return transaction["Номер карты"]
        logger.info("Successfully! Result - %s" % transaction)
    else:
        logger.error("Something went wrong in 'get_card_number' function")
        return None


def total_sum_amount(reader: Any, card_number: Any) -> int:
    """
    Возвращает общую сумму всех транзакций пользователя.
    """
    total = 0
    if card_number:
        for transaction in reader:
            total += transaction["Сумма операции"]
    logger.info("Successfully! Result - %s" % total)
    return round(total)


def get_cashback(total_sum: int) -> int:
    """
    Возвращает весь кешбек
    """
    res = total_sum // 100
    logger.info("Successfully! Result - %s" % res)
    return res


def top_transactions(reader: Any) -> list[dict[str, Any]] | None:
    """
    Возвращает топ-5 транзакций пользователя по сумме.
    """
    if reader is not None:

        def sort_by_sum(item: Any) -> Any:
            return item["Сумма операции"]

        reader.sort(key=sort_by_sum, reverse=True)

        result = []
        i = 0
        for transaction in reader:
            if i < 5:
                result.append(
                    {
                        "date": transaction["Дата операции"],
                        "amount": round(transaction["Сумма операции"]),
                        "category": transaction["Категория"],
                        "description": transaction["Описание"],
                    }
                )
                i += 1
            else:
                break
        logger.info("Successfully! Result - %s" % result)
        return result
    else:
        logger.error("Something went wrong in 'top_transactions' function...")
        return None


def get_currency_rate(currency: Any) -> Any:
    """
    Возвращает курс валюты.
    """
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols=RUB&base={currency}"
    response = requests.get(url, headers={"apikey": api_key}, timeout=15)
    response_data = json.loads(response.text)
    rate = response_data["rates"]["RUB"]
    logger.info("Successfully 'get_currency_rate' operation!")
    return rate


def get_stock_currency(stock: str) -> Any:
    """
    Возвращает курс акции.
    """
    ticker = yf.Ticker(stock)
    todays_data = pd.DataFrame(ticker.history(period="1d"))
    todays_data_dict = todays_data.to_dict(orient="records")
    logger.info("Successfully 'get_stock_currency' operation!")
    return todays_data_dict[0]["High"]


def create_operations(greetin: Any, card_numbers: Any, total_sum: Any, cashbacks: Any, top: Any) -> Any:
    """
    Возвращает словарь с данными пользователя.
    """
    data = {"greeting": greetin, "cards": [], "top_transactions": [], "currency_rates": [], "stock_prices": []}
    if reader_operations:
        for line in reader_operations:
            if card_numbers not in [card["last_digits"] for card in data["cards"]] and card_numbers is not None:
                data["cards"].append(
                    {"last_digits": card_numbers, "total_spent": round(total_sum, 2), "cashback": cashbacks}
                )
        data["top_transactions"] = top
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
        logger.info("Successfully 'create_operations' operation!")
    return data


def main_views() -> None:
    """
    Запускает программу.
    """
    user_currency = input("Which currency would you like append to file?").split(", ")
    user_stock = input("Which stock would you like append to file?").split(", ")
    result = {"currency": user_currency, "stock": user_stock}
    with open("user_settings.json", "w") as f:
        json.dump(result, f, ensure_ascii=False)
    time = input("Write date and time(format for input - DD.MM.YYYY HH:MM):")
    greetin = greeting(time if time else None)
    card_numbers = get_card_number(reader_operations)
    total_sum = total_sum_amount(reader_operations, card_numbers)
    cashbacks = get_cashback(total_sum)
    top = top_transactions(reader_operations)
    created = create_operations(greetin, card_numbers, total_sum, cashbacks, top)
    write_data("new.json", created)
    result = read_files("new.json")
    for key, value in result.items():
        if key == "greeting":
            print(value)
        else:
            print(f"{'' if key == 'greeting' else key}: {value}")


if __name__ == "__main__":
    main_views()
