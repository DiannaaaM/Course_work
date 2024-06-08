import json
import time
from pathlib import Path

import pandas as pd
import requests


def read_xls_file(file_path):
    """Открытие файла с '.xls'"""
    if Path(file_path).suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    else:
        print("Неверный формат файла")
