import datetime
import json
from unittest.mock import patch

import pytest

from src.reports import spending_by_category


@pytest.mark.parametrize("cat_, date_", [("переводы", "2021-12-25")])
def test_spending_by_category_1(fixt_test_df_2, cat_, date_, result_spndg_by_cat_1):
    """Тестирование работы функции с введенной датой"""
    a = spending_by_category(fixt_test_df_2, cat_, date_)
    assert a == result_spndg_by_cat_1


def test_spending_by_category_2(fixt_test_df_2, result_spndg_by_cat_2):
    """Тестирование работы функции без введенной даты"""
    test_now = datetime.datetime(2025, 4, 3, 13, 45, 10)
    with patch("datetime.datetime", wraps=datetime.datetime) as mock_date:
        mock_date.now.return_value = test_now
        a = spending_by_category(fixt_test_df_2, "переводы")
        assert a == result_spndg_by_cat_2


def test_spending_by_category_3(fixt_test_df_2):
    """Отрицательное тестирование функции"""
    with pytest.raises(Exception):
        spending_by_category(fixt_test_df_2, "переводы", "2021-05-32")


def test_log_report_1(fixt_test_df_2, result_spndg_by_cat_1):
    """Положительный тест декоратора на вывод в файл"""
    result = spending_by_category(fixt_test_df_2, "переводы", "2021-12-25")
    with open("./reports/report.json", "r", encoding="utf-8") as file:
        record = json.load(file)
        assert record == result
