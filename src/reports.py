from datetime import datetime, timedelta
from typing import Any, Optional

import pandas as pd

from src.utils import read_files, setup_logging, write_data

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
                write_data("reports.txt", str(result))
                logger.info(f"Successfully operation! Result - {result}")
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
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    total = -transactions[transactions["Категория"] == category]["Сумма операции"].sum()
    logger.info(f"Successfully operation! Result - {round(total, 1)}")
    return round(total, 1)
