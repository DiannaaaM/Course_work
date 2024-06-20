from typing import Any

from pytest import fixture

from src.reports import wastes_by_category
from src.utils import read_files


@fixture()
def date_with_data() -> Any:
    return read_files("../data/operations.xls")


def test_wastes_by_category(date_with_data: Any) -> None:
    result = wastes_by_category(date_with_data, "Супермаркеты")
    assert result == 1000
