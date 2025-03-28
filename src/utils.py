import pandas as pd
from pandas import DataFrame


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

# a = read_excel_file("./data/operations.xlsx")
# print(a.head())
