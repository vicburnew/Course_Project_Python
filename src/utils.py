import pandas as pd
from pandas import DataFrame


def read_excel_file() -> DataFrame:
    """Функция читает данные из файла 'operations.xlsx', расположенного
    в папке ../data и возвращает DataFrame с данными о финансовых транзакциях.
    Если файл пустой, содержит не список или не найден,
    функция возвращает пустой DataFrame."""
    operations_df = DataFrame()

    try:
        operations_df = pd.read_excel("../data/operations.xlsx", na_filter=True)
        # excel_list_result = df_excel.to_dict(orient="records")
    except Exception as ex:
        print(f"Ошибка чтения .excel файла, ошибка: {ex}")
        # excel_list_result = []
    return operations_df

a = read_excel_file()
print(a.head())
