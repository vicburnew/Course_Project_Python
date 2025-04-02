from idlelib.iomenu import encoding

import pandas as pd
from mypy.util import json_loads
from pandas import DataFrame
import json
import datetime

import os

import requests
from dotenv import load_dotenv


def read_excel_file(path_file: str) -> DataFrame:
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


def filter_df_by_date(input_df: DataFrame, input_day_time: str) -> DataFrame:
    """Функция получает на вход DataFrame и строку дату-время в формате YYYY-MM-DD HH:MM:SS
    и возвращает DataFrame, отфильтрованный по датам с начала месяца до введенной даты"""
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
    off_nan_df_filtered_by_dates = off_nan_df[
        (pd.to_datetime(off_nan_df["Дата операции"], dayfirst=True) <= input_day_time_pd) &
        (pd.to_datetime(off_nan_df["Дата операции"], dayfirst=True) > start_day_time_pd)]
    filtered_by_date_df = off_nan_df_filtered_by_dates
    return filtered_by_date_df


def summary_by_card(input_df: DataFrame) -> list[dict]:
    """Функция получает на вход DataFrame и возвращает данные по каждой карте в формате списка словарей:
    - последние 4 цифры карты;
    - общая сумма расходов;
    - кешбэк (1 рубль на каждые 100 рублей)."""
    # Отфильтровываем неудачные ("статус" = "FAILED") операции:
    off_nan_df_filtered_by_status = input_df[(input_df["Статус"]) == "OK"]
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
        dict_for_json_1 = {"last_digits": key, "total_spent": val * -1, "cashback": round(val * 0.01 * -1, 2)}
        list_of_dicts.append(dict_for_json_1)
    # Формируем выход функции:
    summary_by_card_result = list_of_dicts
    return summary_by_card_result


def top_5_transactions(input_df: DataFrame) -> list[dict]:
    """Функция получает на вход DataFrame и возвращает Топ-5 транзакций
    по сумме платежа в формате списка словарей:
      - "date": "21.12.2021",
      - "amount": 1198.23,
      - "category": "Переводы",
       -"description": "Перевод Кредитная карта. ТП 10.2 RUR"""
    # Сортируем df по убыванию суммы платежа:
    off_nan_df_sorted_by_amount = input_df.sort_values("Сумма платежа", ascending=False, inplace=False)
    # Отбираем первые пять трансакций:
    off_nan_df_amount_top_5 = off_nan_df_sorted_by_amount.head()
    # создаем список словарей для передачи в другую функцию:
    list_of_dicts = []
    for index, row in off_nan_df_amount_top_5.iterrows():
        dict_for_json_2 = {"date": str(row["Дата платежа"]), "amount": row["Сумма платежа"],
                           "category": row["Категория"], "description": row["Описание"]}
        list_of_dicts.append(dict_for_json_2)

    top_5_transactions_result = list_of_dicts
    return top_5_transactions_result


def get_currency_rates():
    """Функция считывает данные user_currencies из файла user_settings.json, направляет запрос на
     внешний API и возвращает ответ с текущими курсами валют к рублю в виде списка словарей:
     [{"currency": "USD",
      "rate": 73.21},
    {"currency": "EUR",
      "rate": 87.08}]"""
    # Загружаем данные из файла .env
    load_dotenv()
    # выделяем оттуда ключ API для сервиса APIlayer
    api_key = os.getenv("API_KEY_1")
    # cчитываем данные из файла user_settings.json:
    ## ПРИ ЗАПУСКЕ PYTEST УБРАТЬ ОДНУ ТОЧКУ ИЗ ПУТИ К ФАЙЛУ
    with open("./user_settings.json", "r", encoding="utf-8") as file:
        user_settings_dict = json.load(file)
    # Формируем строку с перечнем валют для передачи в API
    currencies = ",".join(user_settings_dict["user_currencies"])
    # Формируем строку URL
    url = f"https://api.apilayer.com/exchangerates_data/latest?symbols={currencies}&base=RUB"
    headers = {"apikey": api_key}
    # Направляем запрос в API
    response = requests.get(url, headers=headers)
    # Вызываем исключение если был ответ с ошибкой:
    if response.status_code != 200:
        raise Exception("проверьте параметры запроса и повторите его")
    # Получаем ответ в виде словаря:
    result_api_dict = response.json()
    # Выделяем словарь с валютами:
    result_api_dict_curr = result_api_dict["rates"]
    # создаем список словарей для передачи в другую функцию:
    list_of_dicts = []
    for key, val in result_api_dict_curr.items():
        dict_for_json_3 = {"currency": key, "rate": round(1 / val, 2)}
        list_of_dicts.append(dict_for_json_3)
    get_currency_rates_result = list_of_dicts
    return get_currency_rates_result


def get_stock_prices():
    """Функция считывает данные user_stocks из файла user_settings.json, направляет запрос на
     внешний API и возвращает ответ с текущими котировками в виде списка словарей:
      "stock_prices": [{
      "stock": "AAPL",
      "price": 150.12},
    {"stock": "AMZN",
      "price": 3173.18},
    {"stock": "GOOGL",
      "price": 2742.39},
    {"stock": "MSFT",
      "price": 296.71},
    {"stock": "TSLA",
      "price": 1007.08}]"""
    # Загружаем данные из файла .env
    load_dotenv()
    # выделяем оттуда ключ API для сервиса marketstack
    api_key = os.getenv("API_KEY_2")
    # cчитываем данные из файла user_settings.json:
    ## ПРИ ЗАПУСКЕ PYTEST УБРАТЬ ОДНУ ТОЧКУ ИЗ ПУТИ К ФАЙЛУ
    with open("./user_settings.json", "r", encoding="utf-8") as file:
        user_settings_dict = json.load(file)
    # Формируем строку с перечнем валют для передачи в API
    stocks = ",".join(user_settings_dict["user_stocks"])
    # Формируем строку URL
    url = f"https://api.marketstack.com/v1/eod/latest?access_key={api_key}"
    querystring = {"symbols": stocks}
    # Направляем запрос в API
    response = requests.get(url, params=querystring)
    # Вызываем исключение если был ответ с ошибкой:
    if response.status_code != 200:
        raise Exception("проверьте параметры запроса и повторите его")
    # Получаем ответ в виде словаря:
    result_api_stocks_dict = response.json()
    # создаем список словарей для передачи в другую функцию:
    result_api_stocks_dict_list = result_api_stocks_dict["data"]
    list_of_dicts = []
    for record_dict in result_api_stocks_dict_list:
        dict_for_json_4 = {}
        for key, val in record_dict.items():
            if key == "symbol":
                dict_for_json_4["stock"] = val
            if key == "close":
                dict_for_json_4["price"] = val
        list_of_dicts.append(dict_for_json_4)

    get_stock_prices_result = list_of_dicts
    return get_stock_prices_result


# a = read_excel_file("../data/operations.xlsx")
# b = filter_df_by_date(a,"2021-12-23 22:33:11")
# # c = summary_by_card(b)
# # d = top_5_transactions(b)
# print(b)
# # print(c)
# # print(d)
#
# e = get_currency_rates()
# print(e)

# f = get_stock_prices()
# print(f)

# a = off_nan_df_filtered_by_expen.to_json(force_ascii=False, orient="records")
