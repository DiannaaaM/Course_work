import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

import pandas as pd


def setup_logging() -> Logger:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("logs.log", mode="w")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def read_xls_file(file_path: Any) -> Any:
    """Открытие файла '.xls'"""
    if Path(file_path).suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        return df.to_dict(orient="records")
        logger.info("Successfully read file")
    else:
        logger.error("Wrong file format or Something went wrong")
        print("Неверный формат файла")


def write_data(create_operations: Any) -> None:
    """
    Сохраняет словарь с данными пользователя в json файл.
    """
    with open("../data/user_settings.json", "w", encoding="utf8") as f:
        json.dump(create_operations, f, ensure_ascii=False)


def read_user_settings(file_path: Any) -> Any:
    """
    Чтение файла с настройками пользователя.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    logger.info("Successfully read file")


logger = setup_logging()
