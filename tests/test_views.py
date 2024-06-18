import datetime
import unittest
from unittest import TestCase
from src.views import greeting
from pytest import mark


@mark.parametrize("hour, expected", [("07.05.2023 08:00", "Доброе утро"),
                                     ("12.05.2023 13:00", "Добрый день"),
                                     ("20.05.2023 21:00", "Добрый вечер"),
                                     ("23.05.2023 00:00", "Доброй ночи")])
def test_greeting(hour: str, expected: str) -> None:
    assert greeting(hour) == expected


