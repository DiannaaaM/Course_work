from datetime import datetime

import pandas as pd

from src.reports import wastes_by_category
from src.services import filter_by_state
from src.utils import read_files, write_data
from src.views import (
    create_operations,
    get_card_number,
    get_cashback,
    get_currency_rate,
    get_stock_currency,
    greeting,
    top_transactions,
    total_sum_amount,
)


def main() -> None:
    """
    Отвечает за основную логику проекта с пользователем и связывает функциональности между собой.
    """
    reader_operations = read_files("../data/operations.xls")
    # views
    user_currency = input("Which currency would you like append to file?").split(", ")
    user_stock = input("Which stock would you like append to file?").split(", ")
    result = {"currency": user_currency, "stock": user_stock}
    write_data("user_settings.json", result)
    time = input("Write date and time(format for input - DD.MM.YYYY HH:MM):")
    greetin = greeting(time if time else None)
    card_numbers = get_card_number(read_files("../data/operations.xls"))
    total_sum = total_sum_amount(read_files("../data/operations.xls"), card_numbers)
    cashbacks = get_cashback(total_sum)
    top = top_transactions(read_files("../data/operations.xls"))
    created = create_operations(greetin, card_numbers, total_sum, cashbacks, top)
    write_data("new.json", created)

    # servies
    translate = filter_by_state(reader_operations)

    # reports
    df = pd.DataFrame(
        {
            "Дата операции": ["2022-01-05", "2022-02-15", "2022-03-20", "2022-04-10"],
            "Категория": ["food", "entertainment", "food", "transport"],
            "Сумма операции": [50.0, 30.0, 40.0, 20.0],
        }
    )
    print(f'Views result:\n{read_files("new.json")}')
    print(f"Servies result: \n{translate}")
    print(f'Reports result: \n{wastes_by_category(df, "transport", datetime(2022, 4, 10))}')


if __name__ == "__main__":
    main()
