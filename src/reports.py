from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

import pandas as pd

from src.logger import setup_logging
from src.utils import write_data

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
                write_data("reports.json", result)
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
    result: Dict[str, Union[Dict[Any, Any], str, float]] = {}
    three_months_ago = date - timedelta(days=90)
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"])
    total = -transactions[
        (transactions["Дата операции"] >= three_months_ago)
        & (transactions["Дата операции"] <= date)
        & (transactions["Категория"] == category)
    ]["Сумма операции"]
    if total.any():
        result["amount"] = total.to_dict()
        result["category"] = category
        result["total"] = total.sum()

    logger.info(f"Successfully operation! Result - {result}")
    return result


def reports_main() -> None:

    print(f'Reports result: \n{wastes_by_category("../data/operations.xls", "food", datetime(2022, 4, 10))}')
