import json
import re
from pathlib import Path
from typing import Any, List

import pandas as pd
from src.utils import reader_operations


def filter_by_state(transactions):
    """Функция, которая принимает на вход список транзакций
    и возвращает новый список, содержащий только те словари, у которых ключ содержит переданное в функцию значение."""
    result = []
    for transaction in transactions:
        if "Переводы" in transaction["Категория"] and transaction["Описание"].endswith("."):
            result.append(transaction["Описание"])
    return result


translate = filter_by_state(reader_operations)

for i in translate:
    print(i)
