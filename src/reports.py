import json
from typing import Optional
import datetime

import pandas as pd
from pandas import DataFrame
import logging

from src.utils import read_excel_file

# Создание объекта логера для записи событий
logger = logging.getLogger("reports")
logger.setLevel(logging.DEBUG)
# При запуске Pytest исправить путь к имени файла: "./logs/reports.log"
file_handler = logging.FileHandler("../logs/reports.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)


def spending_by_category(input_df: DataFrame, input_cat: str, input_date: Optional[str] = None) -> json:
    """Функция принимает на вход датафрейм с транзакциями, название категории, опциональную дату
    в формате "YYYY-MM-DD".
    Если дата не передана, то берется текущая дата. Функция возвращает строку JSON с тратами по заданной
    категории за последние три месяца (от переданной даты)."""
    logger.info("Начало функций spending_by_category")

    # Определяем исходную дату для выборки
    if input_date is None:
        start_date_obj_0 = datetime.datetime.now()
    else:
        try:
            start_date_obj_0 = datetime.datetime.strptime(input_date, "%Y-%m-%d")
        except Exception as ex:
            logger.error(f"Ошибка ввода даты: {ex}")
            print(f"Ошибка ввода даты: {ex}")
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
    logger.info("Функция spending_by_category завершена успешно")
    return spending_by_category_result



a = read_excel_file("../data/operations.xlsx")
b = spending_by_category(a, "переводЫ", '2021-04-30')
print(b)


