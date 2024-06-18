from datetime import datetime
from typing import Any, Optional

import pandas as pd

from src.utils import read_xls_file

reader_operations = read_xls_file("../data/operations.xls")


def report_to_file(file_name: Optional[str] = None) -> Any:
    def decorator(func: Any) -> Any:
        def wrapper(transactions: pd.DataFrame, category: str, date: Optional[pd.Timestamp] = None) -> Any:
            result = func(transactions, category, date)
            if file_name is None:
                with open("report.txt", "a") as file:
                    file.write(f"{category} total expenses: {result}\n")
            else:
                with open(file_name, "a") as file:
                    file.write(f"{category} total expenses: {result}\n")
            return result

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
    transactions = transactions.query("`Дата операции` >= @date - pd.DateOffset(months=3)")
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
