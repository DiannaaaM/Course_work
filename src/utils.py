import json
from pathlib import Path

import pandas as pd


def read_xls_file(file_path):
    """Открытие файла с '.xls'"""
    if Path(file_path).suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    else:
        print("Неверный формат файла")


reader_operations = read_xls_file("../data/operations.xls")


def read_user_settings(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


reader_settings = read_user_settings("user_settings.json")
