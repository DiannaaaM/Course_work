import json
from pathlib import Path
from typing import Any

import pandas as pd

from src.logger import setup_logging

logger = setup_logging()


def read_files(file_path: Any) -> Any:
    """Открытие файла '.xls'"""
    if Path(file_path).suffix.lower() == ".xls":
        df = pd.read_excel(file_path)
        logger.info("Successfully read file")
        return df.to_dict(orient="records")
    elif Path(file_path).suffix.lower() == ".json":
        with open(file_path, "r", encoding="utf-8") as f:
            logger.info("Successfully read file")
            return json.load(f)
    else:
        logger.error("Wrong file format or Something went wrong")
        print("Неверный формат файла")


def write_data(file_: str, results: Any) -> None:
    """
    Функция, которая записывает результаты в указанный файл.
    """
    try:
        if file_.endswith(".txt"):
            with open(file_, "a") as file:
                file.write(results)
        else:
            with open(file_, "w", encoding="utf8") as f:
                json.dump(results, f, indent=4, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Ошибка при записи файла {file_}: {e}")
