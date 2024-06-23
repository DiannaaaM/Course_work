from src.utils import setup_logging, write_data

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
