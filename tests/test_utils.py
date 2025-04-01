import pandas as pd
from unittest.mock import patch
from unittest import mock
from datetime import date, datetime
import datetime

from coverage.html import read_data

from src.utils import read_excel_file, time_of_a_day, summary_by_card
import pytest


# Тестирование функции read_excel_file

mock_data_df = pd.DataFrame({"Дата операции": ["31.12.2021 16:44:00"], "Дата платежа": ["31.12.2021"], "Номер карты": ["*7197"], "Статус":["OK"]})

def test_read_excel_file_1(mock_excel_dict_fixt):
    """Положительный тест на чтение excel файла"""
    with patch("pandas.read_excel", read_data=mock_data_df) as mock_df:
        pd.read_excel.return_value = mock_data_df
        result = read_excel_file("fake_file.xlsx")
        result_dict = result.to_dict(orient="records")
    assert result_dict == mock_excel_dict_fixt
    mock_df.assert_called()


def test_read_excel_file_2():
    """Отрицательный тест на открытие excel файла"""
    with pytest.raises(Exception) as ex_info:
        read_excel_file("./data/operatons.xlsx")
        assert str(ex_info.value) == "Ошибка чтения .excel файла, ошибка: [Errno 2] No such file or directory: './data/operatons.xlsx'"


# Тестирование функции time_of_a_day

@pytest.mark.parametrize("mock_in, mock_output", [
    (5, "ночь"),
    (0, "ночь"),
    (12, "день"),
    (17, "день"),
    (23, "вечер"),
    (18, "вечер"),
    (6, "утро"),
    (11, "утро")])

def test_time_of_a_day(mock_in, mock_output):
    """Тестирование функции возврата текущего времени суток"""
    test_now = datetime.datetime(2024, 10, 10, mock_in, 10, 10)
    with patch("datetime.datetime", wraps=datetime.datetime) as mock_date:
        mock_date.now.return_value = test_now
        result_1, result_2 = time_of_a_day()
        assert  result_1 == mock_output

# Тестирование функции summary_by_card

def test_summary_by_card_1(fixt_test_df, fixt_card_result):
    """Положительное тестирование функции выдачи сводных данных по картам"""
    a = summary_by_card(fixt_test_df, "2021-12-24 14:58:38")
    assert a == fixt_card_result

def test_summary_by_card_2(fixt_test_df):
    """Отрицательное тестирование функции выдачи сводных данных по картам"""
    with pytest.raises(Exception):
        a = summary_by_card(fixt_test_df,"2021-05-32 14:58:38" )

