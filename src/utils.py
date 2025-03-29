import pandas as pd
from pandas import DataFrame
import json
import datetime





def read_excel_file(path_file:str) -> DataFrame:
    """Функция читает данные из файла 'operations.xlsx', расположенного
    в папке ../data и возвращает DataFrame с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден,
    функция возвращает пустой DataFrame."""
    operations_df = DataFrame()
    try:
        operations_df = pd.read_excel(path_file, na_filter=True)
    except Exception as ex:
        print(f"Ошибка чтения .excel файла, ошибка: {ex}")
    return operations_df


def time_of_a_day() -> tuple:
    """Функция возвращает два значения:
    a) текущее время суток - "утро", "день", "вечер", "ночь.
    (Принята следующая система: с 0 до 6 часов — ночь, с 6 до 12 часов — утро,
    с 12 до 18 часов — день, с 18 до 24 часов — вечер) и
    b) текущая дата и время как список строк"""
    date_hour_obj = datetime.datetime.now()
    # print(date_hour_obj)
    date_hour_str = datetime.datetime.strftime(date_hour_obj, "%Y %m %d %H %M %S")
    date_of_now_list = date_hour_str.split()
    if 18 <= int(date_of_now_list[3]) <= 24:
        time_of_day_now = "вечер"
    elif 12 <= int(date_of_now_list[3]) < 18:
        time_of_day_now = "день"
    elif 6 <= int(date_of_now_list[3]) < 12:
        time_of_day_now = "утро"
    else:
        time_of_day_now = "ночь"
    return time_of_day_now, date_of_now_list



a, b = time_of_a_day()
print(a, b)

