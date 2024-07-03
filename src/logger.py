import logging
from logging import Logger


def setup_logging() -> Logger:
    """
    Функция, которая настраивает логирование.
    """
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(module)s - %(levelname)s - %(message)s", encoding="utf-8"
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("logs.log", mode="w")
    file_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(module)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    return logger
