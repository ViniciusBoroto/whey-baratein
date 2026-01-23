from unittest.mock import Mock

import pytest

from application.usecase.delete_user_usecase import DeleteUserUseCase
from domain.exception import UserNotFoundException


def test_delete_user():
    mock_user_repo = Mock()
    mock_user_repo.delete_user.return_value = None

    uc = DeleteUserUseCase(mock_user_repo)
    result = uc.Execute(1)
    
    assert result is None
    mock_user_repo.delete_user.assert_called_once_with(1)


def test_delete_user_not_found():
    mock_user_repo = Mock()
    mock_user_repo.delete_user.side_effect = UserNotFoundException(999)

    uc = DeleteUserUseCase(mock_user_repo)
    
    with pytest.raises(UserNotFoundException):
        uc.Execute(999)
