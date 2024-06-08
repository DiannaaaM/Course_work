from src.utils import reader
import pandas as pd


def wastes_by_category(transactions: pd.DataFrame, category: str):
    total = 0.0
    for transaction in transactions:
        if transaction["Категория"] == category:
            total += transaction["Сумма операции"] * -1
    return round(total, 1)


print(wastes_by_category(reader, "Супермаркеты"))
