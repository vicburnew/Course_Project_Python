from idlelib.iomenu import encoding

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
        # operations_df = pd.read_excel(path_file, na_filter=True, parse_dates=[1], date_format="%d.%m.%Y %H:%M:%S")
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


def summary_by_card(input_df: DataFrame, input_day_time:str) -> list[dict]:
    """Функция получает на вход DataFrame и строку дату-время в формате YYYY-MM-DD HH:MM:SS
     и возвращает данные по каждой карте в формате JSON:
    - последние 4 цифры карты;
    - общая сумма расходов;
    - кешбэк (1 рубль на каждые 100 рублей)."""
    # Очищаем DataFrame от пустых (Nan) полей, заменяем их на 0
    off_nan_df = input_df.fillna(value=0, inplace=False)
    # Переводим строку с датой в формат pandas
    try:
        input_day_time_pd = pd.to_datetime(input_day_time, dayfirst=False)
    except Exception as ex:
        print(f"Ошибка ввода даты: {ex}")
    # Определяем начальную дату для фильтрации:
        ## Выделяем год и переводим в строку
    start_year_str = str(input_day_time_pd.year)
        ## Выделяем месяц и переводим в строку
    start_month_str = str(input_day_time_pd.month)
        ## Формируем полную строку
    start_date_str = start_year_str + "-" + start_month_str + "-" + "01"
        ## Переводим ее в формат pd_time
    start_day_time_pd = pd.to_datetime(start_date_str)
    # Производим выборку (фильтрацию) df по заданной и начальной датам:
    off_nan_df_filtered_by_dates = off_nan_df[(pd.to_datetime(off_nan_df["Дата операции"], dayfirst=True) < input_day_time_pd) &
                   (pd.to_datetime(off_nan_df["Дата операции"], dayfirst=True) > start_day_time_pd)]
    # Отфильтровываем неудачные ("статус" = "FAILED") операции:
    off_nan_df_filtered_by_status = off_nan_df_filtered_by_dates[(off_nan_df_filtered_by_dates["Статус"]) == "OK"]
    # Отфильтровываем строки с отсутствующими номерами карт ("номер карты" = "0"):
    off_nan_df_filtered_by_cards = off_nan_df_filtered_by_status[(off_nan_df_filtered_by_status["Номер карты"]) != 0]
    # Отфильтровываем строки с "положительным расходом" ("Сумма платежа" > 0):
    off_nan_df_filtered_by_expen = off_nan_df_filtered_by_cards[(off_nan_df_filtered_by_cards["Сумма платежа"]) < 0]
    # Группируем и агрегируем сумму расходов по картам:
    cards_and_expen_values_df = off_nan_df_filtered_by_expen.groupby("Номер карты").agg({"Сумма платежа": "sum"})
    # Переводим в словарь пары "ключ - номер карты", "значение - величина расходов", убирая ключ "Сумма платежа"
    cards_and_expen_values_dict = cards_and_expen_values_df.to_dict()["Сумма платежа"]
    # создаем список словарей для передачи в другую функцию:
    list_of_dicts = []
    for key, val in cards_and_expen_values_dict.items():
        dict_for_json_1 = {}
        dict_for_json_1["last_digits"] = key
        dict_for_json_1["total_spent"] = val * -1
        dict_for_json_1["cashback"] = round(val * 0.01 *-1, 2)
        list_of_dicts.append(dict_for_json_1)
    # Формируем выход функции:
    summary_by_card_result = list_of_dicts
    return summary_by_card_result


# a = read_excel_file("../data/operations.xlsx")
# b = summary_by_card(a,"2019-12-24 14:58:38")
# print(b)



# a = off_nan_df_filtered_by_expen.to_json(force_ascii=False, orient="records")