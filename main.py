import time
from pathlib import Path
from typing import Any

from src.external_api import get_currency_rate
from src.generators import filter_by_currency, random_card_number, returned_description
from src.libraries import count_categories, filter_by_state
from src.logger import setup_logging
from src.masks import mask_account, mask_card
from src.processing import sort_dicts_by_date, sorted_list_by_value
from src.reader_csv_xlsx_files import open_file
from src.utils import read_json_file, sum_amount
from src.widget import get_data, mask_account_and_card


def main(
    user_input: str, type_of_sort: str, currency: Any = None, sort_of_date: Any = None, filter_by_word: Any = None
) -> Any:
    """
    Отвечает за основную логику проекта с пользователем и связывает функциональности между собой.
    """
    if user_input == "1":
        file = read_json_file(Path("data/operations.json"))
    elif user_input == "2":
        file = open_file(Path("data/transactions.csv"))
    else:
        file = open_file(Path("data/transactions_excel.xlsx"))

    sort = sorted_list_by_value(file, type_of_sort.upper())

    if sort_of_date is not None:
        reverse_value = "asc" if sort_of_date.lower() == "1" else "desc"
        sort = sort_dicts_by_date(sort, reverse_value)

    if currency.lower() == "да":
        for value in sort:
            sort = value.get("operationAmount", {}).get("amount", {}) * get_currency_rate(
                value.get("operationAmount", {}).get("currency_code", {})
            )

    if filter_by_word is not None:
        sort = filter_by_state(sort, filter_by_word)
    print(sort)

    result = []
    for value in sort:
        date = get_data(value.get("date", ""))
        description = value["description"]
        from_ = mask_account_and_card(str(value.get("from", "")))
        to = mask_account_and_card(value.get("to", ""))
        if "operationAmount" in value or "amount" in value:
            amount = sum_amount(value)
        else:
            amount = "0.0"

        # Создание строки с форматированием для  улучшения читаемости
        transaction_string = f"{date} {description}\n{from_} -> {to}\nСумма: {amount}\n"
        result.append(transaction_string)

    return result


print(
    """Привет! Добро пожаловать в программу работы с банковскими транзакциями. 
Выберите необходимый пункт меню:
1. Получить информацию о транзакциях из json файла
2. Получить информацию о транзакциях из csv файла
3. Получить информацию о транзакциях из xlsx файла"""
)
user_input = input("выберите\t\t")
if user_input not in ["1", "2", "3"]:
    print("Но такого варианта нет... " "\nПопробуйте еще раз")

type_of_sort = input(
    """Введите статус по которому необходимо выполнить фильтрацию. 
Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"""
)
verification_date = input("Отсортировать операции по дате? Да/Нет").lower()
sort_of_date = None
if verification_date == "да":
    sort_of_date = input("Отсортировать по:" "\n1. возрастанию" "\n2. убыванию")

user_currency = input("Выводить только рублевые тразакции? Да/Нет")
Verification_filter_of_word = input(
    "Отфильтровать список транзакций по определенному слову в описании? Да/Нет"
).capitalize()
filter_by_word = None
if Verification_filter_of_word == "Да":
    filter_by_word = input("Введите описание, по которому необходимо отсортировать\n").capitalize()

result = main(user_input, type_of_sort, user_currency, sort_of_date, filter_by_word)
print("Распечатываю итоговый список транзакций...")
time.sleep(1)
print(*result, sep="\n")
