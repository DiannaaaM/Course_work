import json
import logging
from logging import Logger
from pathlib import Path
from typing import Any

import pandas as pd


def setup_logging() -> Logger:
    """
    Функция, которая настраивает логирование.
    """
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s", encoding="utf-8")
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("logs.log", mode="w")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger


def read_files(file_path: Any) -> Any:
    """Открытие файла '.xls'"""
    if Path(file_path).suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        logger.info("Successfully read file")
        return df.to_dict(orient="records")
    elif Path(file_path).suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
        logger.info("Successfully read file")
    else:
        logger.error("Wrong file format or Something went wrong")
        print("Неверный формат файла")


def write_data(filename: Any, create_operations: Any) -> None:
    """
    Сохраняет словарь с данными пользователя в json файл.
    """
    if filename.endswith(".txt"):
        with open(filename, "a") as file:
            file.write(create_operations)
    else:
        with open(filename, "w", encoding="utf8") as f:
            json.dump(create_operations, f, indent=4, ensure_ascii=False)


logger = setup_logging()
