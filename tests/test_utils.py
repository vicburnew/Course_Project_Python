import pandas as pd
from unittest.mock import mock_open, patch
from src.utils import read_excel_file
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



