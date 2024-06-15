import json
from pathlib import Path
import logging
import pandas as pd


def read_xls_file(file_path):
    """Открытие файла '.xls'"""
    if Path(file_path).suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    else:
        print("Неверный формат файла")


reader_operations = read_xls_file("../data/operations.xls")


def read_user_settings(file_path):
    """

    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


reader_settings = read_user_settings("user_settings.json")


def setup_logging():
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger