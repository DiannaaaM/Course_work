import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

import pandas as pd


def read_xls_file(file_path: Any) -> Any:
    """Открытие файла '.xls'"""
    if Path(file_path).suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
    else:
        print("Неверный формат файла")


def read_user_settings(file_path: Any) -> Any:
    """ """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def setup_logging() -> Logger:
    logger = logging.getLogger(__name__)
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(lineno)d: %(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    logger.setLevel(logging.INFO)
    return logger


reader_operations = read_xls_file("../data/operations.xls")
reader_settings = read_user_settings("user_settings.json")
