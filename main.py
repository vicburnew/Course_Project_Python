from src.utils import read_excel_file


def main() -> None:
    """Реализация основного функционала программы"""
    # Вызов функции чтения исходного файла .xlsx, содержащего исходные транзакции
    initial_df = read_excel_file("./data/operations.xlsx")

    return None

if __name__ == '__main__':
    main()

