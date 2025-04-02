import json
import re
import pandas as pd
from pandas import DataFrame

from src.utils import read_excel_file

pd.options.mode.copy_on_write = True


def transfers_to_people(input_df: DataFrame) -> json:
    """Функция получает на вход DataFrame и возвращает JSON-ответ со всеми транзакциями,
    которые относятся к переводам физлицам. Категория такой транзакции — Переводы,
    а в описании есть имя и первая буква фамилии с точкой.
    Например:
    Валерий А.
    Сергей З.
    Артем П."""

    # Фильтруем df по категории "переводы":
    transactions_df = input_df[input_df["Категория"] == "Переводы"]
    # Переводим отфильтрованный df в словарь:
    transactions_dict = transactions_df.to_dict(orient="records")
    # Формируем паттерн для поиска имен:
    pattern_obj = re.compile(r"\b\w+\b\s\b\w\.")
    # Ищем строки с именами по ключу "описание":
    list_of_people = []
    for dict_ in transactions_dict:
        match = pattern_obj.search(dict_["Описание"])
        if match:
            list_of_people.append(dict_)
    # переводим словарь в формат JSON:
    result_json = json.dumps(list_of_people, ensure_ascii=False, indent=4)
    return result_json

# print(transfers_to_people())
