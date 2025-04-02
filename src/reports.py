import json
from typing import Optional
import datetime

import pandas as pd
from pandas import DataFrame

from src.utils import read_excel_file


def spending_by_category(input_df: DataFrame, input_cat: str, input_date: Optional[str] = None) -> json:
    """Функция принимает на вход датафрейм с транзакциями, название категории, опциональную дату
    в формате "YYYY-MM-DD".
    Если дата не передана, то берется текущая дата. Функция возвращает DataFrame по заданной
    категории за последние три месяца (от переданной даты)."""

    # Определяем исходную дату для выборки
    if input_date is None:
        start_date_obj_0 = datetime.datetime.now()
    else:
        start_date_obj_0 = datetime.datetime.strptime(input_date, "%Y-%m-%d")
    # Изменяем в объекте времени-даты время на максимальное:
    start_date_obj = start_date_obj_0.replace(hour=23, minute=59, second=59)
    # Определяем конечную дату для выборки (минус три месяца = 90 дней)
    end_date_obj = start_date_obj - datetime.timedelta(days=90)
    start_date_pd = pd.to_datetime(start_date_obj)
    end_date_pd = pd.to_datetime(end_date_obj)
    # Производим выборку (фильтрацию) df по заданной и начальной датам:
    df_filtered_by_dates = input_df[
        (pd.to_datetime(input_df["Дата операции"], dayfirst=True) <= start_date_pd)
        & (pd.to_datetime(input_df["Дата операции"], dayfirst=True) >= end_date_pd)
        ]
    # Производим выборку (фильтрацию) df по заданной категории:
    df_filtered_by_cat = df_filtered_by_dates[df_filtered_by_dates["Категория"] == input_cat.title()]
    # Отфильтровываем строки с "положительным расходом" ("Сумма платежа" > 0):
    df_filtered_by_cat_expns = df_filtered_by_cat[df_filtered_by_cat["Сумма платежа"] < 0]
    # Вычисляем сумму трат по заданной категории:
    sum_exp = df_filtered_by_cat_expns.agg({"Сумма платежа":"sum"}) * -1
    sum_exp_float = round(float(sum_exp.iloc[0]), 2)
    # Формируем строку для вывода ответа JSON:
    result_dict = {"category":input_cat,
                    "start_date":str(start_date_pd),
                    "end_date":str(end_date_pd),
                    "total_expenses":sum_exp_float
                   }
    spending_by_category_result = json.dumps(result_dict, ensure_ascii=False, indent=4)
    return spending_by_category_result



a = read_excel_file("../data/operations.xlsx")
b = spending_by_category(a, "фастфуд", '2021-04-30')
print(b)


