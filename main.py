from src.reports import spending_by_category
from src.services import transfers_to_people
from src.utils import read_excel_file
from src.views import main_user_interface


if __name__ == '__main__':
    result_1 = main_user_interface("2021-12-21 13:04:15")
    result_2 = read_excel_file("./data/operations.xlsx")
    result_3 = transfers_to_people(result_2)
    result_4 = spending_by_category(result_2, "переводы", '2021-04-30')
    print(result_1)
    print(result_3)
    print(result_4)


