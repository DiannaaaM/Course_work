import re
from pathlib import Path
from typing import Any, List
import pandas as pd
import json


def open_file(file_path: str) -> List[dict]:
    """Открытие файла с '.xls'"""
    file_path = Path(file_path)
    if file_path.suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    else:
        return "Неверный формат файла"


with open("f.json", "w", encoding='utf-8') as f:
    json.dump(open_file('../data/operations.xls'), f, ensure_ascii=False)

def filter_by_state(transactions: Any, search: str) -> list:
    """Функция, которая принимает на вход список словарей и значение для ключа
    и возвращает новый список, содержащий только те словари, у которых ключ содержит переданное в функцию значение."""
    result = []
    for transaction in transactions:
        f = re.search(search, transaction["описание"])
        result.append(f)
    return result


print(filter_by_state('../src/f.json', "Ситидрайв"))

