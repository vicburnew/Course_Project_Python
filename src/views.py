import json

from src.utils import read_excel_file, filter_df_by_date, time_of_a_day, summary_by_card, top_5_transactions, \
    get_currency_rates, get_stock_prices


# В данном модуле реализованы основные функции для генерации JSON-ответов

def main_user_interface(date_time_request: str) -> json:
    """Функция, принимающая на вход строку с датой и временем в формате YYYY-MM-DD HH:MM:SS
    и возвращающая JSON-ответ со следующими данными:
    1. Приветствие в формате "???", где ??? — «Доброе утро» / «Добрый день» / «Добрый вечер» / «Доброй ночи»
    в зависимости от текущего времени.
    2. По каждой карте:
        последние 4 цифры карты;
        общая сумма расходов;
        кешбэк (1 рубль на каждые 100 рублей).
    3. Топ-5 транзакций по сумме платежа.
    4. Курс валют.
    5. Стоимость акций из S&P500.
    """
    # Вызываем функцию чтения текущего времени суток:
    greeting = time_of_a_day()
    # Вызываем функцию чтения исходного excel-файла:
    initial_df = read_excel_file("../data/operations.xlsx")
    # Вызываем функцию фильтрации полученного DataFrame по датам:
    dates_filtered_df = filter_df_by_date(initial_df, date_time_request)
    # Вызываем функцию суммирования операций по картам:
    cards_summary_list = summary_by_card(dates_filtered_df)
    # Вызываем функцию получения 5 самых крупных транзакций:
    top_5_transactions_list = top_5_transactions(dates_filtered_df)
    # Вызываем функцию получения курсов валют:
    curr_rates_list = get_currency_rates()
    # Вызываем функцию получения курсов акций:
    stock_prices_list = get_stock_prices()
    # создаем словарь для вывода результата:
    result_dict = {"greeting": greeting,
                   "cards": cards_summary_list,
                   "top_transactions": top_5_transactions_list,
                   "currency_rates": curr_rates_list,
                   "stock_prices": stock_prices_list}
    # переводим словарь в формат JSON:
    result_json = json.dumps(result_dict, ensure_ascii=False, indent=4)

    return result_json

#
# a = main_user_interface("2021-12-21 13:04:15")
# print(a)
