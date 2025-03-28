import pytest
import pandas as pd

@pytest.fixture
def mock_excel_dict_fixt():
    return [{'Дата операции': '31.12.2021 16:44:00',
  'Дата платежа': '31.12.2021',
  'Номер карты': '*7197',
  'Статус': 'OK'}]
