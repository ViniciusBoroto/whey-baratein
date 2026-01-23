from unittest.mock import Mock

from application.usecase.delete_whey_usecase import DeleteWheyUseCase


def test_delete_whey():
    mock_whey_repo = Mock()
    mock_whey_repo.delete_whey.return_value = None

    uc = DeleteWheyUseCase(mock_whey_repo)
    result = uc.Execute("123")
    
    assert result is None
    mock_whey_repo.delete_whey.assert_called_once_with("123")


import pytest
from domain.exception import WheyNotFoundException


def test_delete_whey_not_found():
    mock_whey_repo = Mock()
    mock_whey_repo.delete_whey.side_effect = WheyNotFoundException("999")

    uc = DeleteWheyUseCase(mock_whey_repo)
    
    with pytest.raises(WheyNotFoundException):
        uc.Execute("999")
