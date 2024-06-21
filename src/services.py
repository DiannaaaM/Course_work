from src.utils import read_files, setup_logging, write_data

reader_operations = read_files("data/operations.xls")
logger = setup_logging()


def filter_by_state(transactions: list[dict]) -> list:
    """Функция, которая принимает на вход список транзакций
    и возвращает новый список, содержащий только те словари, у которых ключ содержит переданное в функцию значение."""
    result = []
    for transaction in transactions:
        if "Переводы" in transaction["Категория"] and transaction["Описание"].endswith("."):
            result.append(transaction["Описание"])
    logger.info("Successfully! Result - %s" % result)
    write_data("results.json", f"Переводы: {result}")
    return result


translate = filter_by_state(reader_operations)


def main_servies() -> None:
    """
    Функция выводит на печать список транзакций, соответствующих указанным критериям.
    """
    print(" ".join(translate))


if __name__ == "__main__":
    main_servies()
