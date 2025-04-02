import pandas as pd
from unittest.mock import patch
import datetime


from src.utils import (
    read_excel_file,
    time_of_a_day,
    summary_by_card,
    filter_df_by_date,
    top_5_transactions,
    get_currency_rates,
    get_stock_prices,
)
import pytest


# Тестирование функции read_excel_file
mock_data_df = pd.DataFrame(
    {
        "Дата операции": ["31.12.2021 16:44:00"],
        "Дата платежа": ["31.12.2021"],
        "Номер карты": ["*7197"],
        "Статус": ["OK"],
    }
)


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
        assert (
            str(ex_info.value)
            == "Ошибка чтения .excel файла, ошибка: [Errno 2] No such file or directory: './data/operatons.xlsx'"
        )


# Тестирование функции time_of_a_day
@pytest.mark.parametrize(
    "mock_in, mock_output",
    [
        (5, "Доброй ночи"),
        (0, "Доброй ночи"),
        (12, "Добрый день"),
        (17, "Добрый день"),
        (23, "Добрый вечер"),
        (18, "Добрый вечер"),
        (6, "Доброе утро"),
        (11, "Доброе утро"),
    ],
)
def test_time_of_a_day(mock_in, mock_output):
    """Тестирование функции возврата текущего времени суток"""
    test_now = datetime.datetime(2024, 10, 10, mock_in, 10, 10)
    with patch("datetime.datetime", wraps=datetime.datetime) as mock_date:
        mock_date.now.return_value = test_now
        result_1 = time_of_a_day()
        assert result_1 == mock_output


# Тестирование функции filter_df_by_date
def test_filter_df_by_date(fixt_test_df, fixt_test_df_dict):
    """Положительное тестирование функции"""
    result = filter_df_by_date(fixt_test_df, "2021-12-25 13:04:15")
    result_dict = result.to_dict(orient="records")
    assert result_dict == fixt_test_df_dict


def test_filter_df_by_date_2(fixt_test_df, fixt_test_df_dict):
    """Отрицательное тестирование функции"""
    with pytest.raises(Exception):
        filter_df_by_date(fixt_test_df, "2021-05-32 13:04:15")


# Тестирование функции summary_by_card
def test_summary_by_card_1(fixt_test_df, fixt_card_result):
    """Тестирование функции выдачи сводных данных по картам"""
    result = summary_by_card(fixt_test_df)
    assert result == fixt_card_result


# Тестирование функции top_5_transactions
def test_top_5_transactions(fixt_test_df, fixt_top_5_results):
    """Тестирование функции выдачи первых 5 максимальных транзакций"""
    result = top_5_transactions(fixt_test_df)
    assert result == fixt_top_5_results


# Тестирование функции get_currency_rates
@patch("requests.get")
def test_get_currency_rates_1(mocked_get):
    """Тестирование функции вывода текущих значений курсов валют"""
    # ПРИ ЗАПУСКЕ PYTEST УБРАТЬ ОДНУ ТОЧКУ ИЗ ПУТИ К ФАЙЛУ user_settings.json
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = {
        "success": True,
        "timestamp": 1743512704,
        "base": "RUB",
        "date": "2025-04-01",
        "rates": {"USD": 0.011778, "EUR": 0.010921},
    }
    result = get_currency_rates()
    assert result == [{"currency": "USD", "rate": 84.9}, {"currency": "EUR", "rate": 91.57}]


@patch("requests.get")
def test_get_currency_rates_2(mocked_get):
    """Отрицательный тест на работу функции - код возврата не равен 200"""
    mocked_get.return_value.status_code = 201
    with pytest.raises(Exception):
        get_currency_rates()


# Тестирование функции get_stock_prices


@patch("requests.get")
def test_get_stock_prices_1(mocked_get, api_stocks_response, get_stocks_mock_result):
    """Тестирование функции вывода текущих значений курсов акций"""
    # ПРИ ЗАПУСКЕ PYTEST УБРАТЬ ОДНУ ТОЧКУ ИЗ ПУТИ К ФАЙЛУ user_settings.json
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.json.return_value = api_stocks_response
    result = get_stock_prices()
    assert result == get_stocks_mock_result


@patch("requests.get")
def test_get_stock_prices_2(mocked_get):
    """Отрицательный тест на работу функции - код возврата не равен 200"""
    mocked_get.return_value.status_code = 201
    with pytest.raises(Exception):
        get_stock_prices()
