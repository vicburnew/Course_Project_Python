from unittest.mock import patch

from src.services import transfers_to_people


def test_transfers_to_people_1(fixt_test_df_2, mock_result_trsnf_people):
    """Тестирование на корректную фильтрацию"""
    result = transfers_to_people(fixt_test_df_2)
    assert result == mock_result_trsnf_people

