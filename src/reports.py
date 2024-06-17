from typing import Optional, Any

import pandas as pd

from src.utils import reader_operations


def wastes_by_category(transactions: pd.DataFrame, category: str, date: Optional[pd.Timestamp] = None) -> Any:
    """ """
    if date is None:
        date = pd.to_datetime("today")
    else:
        date = pd.to_datetime(date)
    transactions = transactions.query("Дата операции >= @date - pd.DateOffset(months=3)")
    total = -transactions[transactions["Категория"] == category]["Сумма_операции"].sum()
    return round(total, 1)


print(wastes_by_category(reader_operations, "Супермаркеты"))
print(wastes_by_category(reader_operations, "Супермаркеты", pd.to_datetime("2021-01-01")))