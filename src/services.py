import json
import re
import pandas as pd
from pandas import DataFrame
import logging

pd.options.mode.copy_on_write = True

# Создание объекта логера для записи событий
logger = logging.getLogger("services")
logger.setLevel(logging.DEBUG)
# При запуске Pytest исправить путь к имени файла: "./logs/utils.log"
file_handler = logging.FileHandler("./logs/services.log", "w", encoding="utf-8")
file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

def transfers_to_people(input_df: DataFrame) -> json:
    """Функция получает на вход DataFrame и возвращает JSON-ответ со всеми транзакциями,
    которые относятся к переводам физлицам. Категория такой транзакции — Переводы,
    а в описании есть имя и первая буква фамилии с точкой.
    Например:
    Валерий А.
    Сергей З.
    Артем П."""

    logger.info("Начало функций transfers_to_people")
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
    logger.info("Функция transfers_to_people завершена успешно")
    return result_json


