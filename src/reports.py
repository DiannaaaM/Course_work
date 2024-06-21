from datetime import datetime, timedelta
from typing import Any, Optional

import pandas as pd

from src.utils import setup_logging, write_data

# reader_operations = read_files("../data/operations.xls")
logger = setup_logging()


def report_to_file() -> Any:
    """
    Функция, которая принимает на вход список транзакций
    и возвращает новый список, содержащий только те словари, у которых ключ содержит переданное в функцию значение.
    """

    def decorator(func: Any) -> Any:
        def wrapper(transactions: pd.DataFrame, category: str, date: Optional[pd.Timestamp] = None) -> Any:
            try:
                result = func(transactions, category, date)
                write_data("reports.txt", result)
                return result
            except Exception as e:
                logger.error(f"Ошибка в функции {func.__name__}: {e}")
                return None

        return wrapper

    return decorator


@report_to_file()
def wastes_by_category(transactions: pd.DataFrame, category: str, date: Optional[pd.Timestamp] = None) -> Any:
    """Функция, которая принимает на вход список транзакций
    и возвращает новый список, содержащий только те словари, у которых ключ содержит переданное в функцию значение."""
    transactions = pd.DataFrame(transactions)
    if date is None:
        date = pd.to_datetime("today")
    else:
        date = pd.to_datetime(date)

    three_months_ago = date - timedelta(days=90)
    transactions = transactions[transactions["Дата операции"] >= three_months_ago]
    total = -transactions[transactions["Категория"] == category]["Сумма операции"].sum()
    return round(total, 1)


def main_reports() -> None:
    """
    Функция, которая выводит на экран сумму потраченных денег на каждую категорию.
    """
    df = pd.DataFrame(
        {
            "Дата операции": ["2022-01-05", "2022-02-15", "2022-03-20", "2022-04-10"],
            "Категория": ["food", "entertainment", "food", "transport"],
            "Сумма операции": [50.0, 30.0, 40.0, 20.0],
        }
    )
    print(wastes_by_category(df, "food", datetime(2022, 4, 10)))


if __name__ == "__main__":
    main_reports()
