
from typing import Any
import os
import pandas as pd
from pytest import fixture
from pathlib import Path
from src.reports import wastes_by_category
from src.utils import read_files
from datetime import datetime


@fixture()
def date_with_data() -> Any:
    return pd.DataFrame(
        {
            "Дата операции": ["2022-01-05", "2022-02-15", "2022-03-20", "2022-04-10"],
            "Категория": ["food", "entertainment", "food", "transport"],
            "Сумма операции": [50.0, 30.0, 40.0, 20.0],
        }
    )
    wastes_by_category(df, "food", datetime(2022, 4, 10))


def test_wastes_by_category(date_with_data: Any) -> None:
    result = wastes_by_category(date_with_data, "food", datetime(2022, 4, 10))
    assert result == None

