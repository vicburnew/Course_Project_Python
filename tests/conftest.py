import pytest
import pandas as pd


@pytest.fixture
def mock_excel_dict_fixt():
    return [{'Дата операции': '31.12.2021 16:44:00',
             'Дата платежа': '31.12.2021',
             'Номер карты': '*7197',
             'Статус': 'OK'}]


@pytest.fixture
def fixt_card_result():
    return [{'cashback': 0.02, 'last_digits': '*5091', 'total_spent': 1.51}]

@pytest.fixture
def fixt_test_df():
    return pd.DataFrame({"Дата операции":["25.12.2021 13:04:15",
                                         "24.12.2021 15:44:07",
                                         "23.12.2021 22:33:11",
                                         "23.12.2021 16:45:12",
                                         "14.11.2021 14:46:24"],
                        "Номер карты":["*7197", "","*5091","*4556","*4556"],
                        "Статус":["OK","OK","OK","OK","FAILED"],
                         "Сумма платежа":[-3400.00,-2000.00,-1.51,20000.00,-55.00]})

