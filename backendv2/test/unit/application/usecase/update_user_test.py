from unittest.mock import Mock

import pytest

from application.usecase.update_user_usecase import UpdateUserUseCase
from domain.entity.user import User
from domain.exception import UserNotFoundException


def test_update_user():
    updated_user = User(id=1, name="updated_name", email="updated@email.com", password="hashed_password")
    
    mock_user_repo = Mock()
    mock_user_repo.update_user.return_value = updated_user

    uc = UpdateUserUseCase(mock_user_repo)
    result = uc.Execute(1, "updated_name", "updated@email.com")
    
    assert result.id == 1
    assert result.name == "updated_name"
    assert result.email == "updated@email.com"
    mock_user_repo.update_user.assert_called_once_with(1, "updated_name", "updated@email.com")


def test_update_user_not_found():
    mock_user_repo = Mock()
    mock_user_repo.update_user.side_effect = UserNotFoundException(999)

    uc = UpdateUserUseCase(mock_user_repo)
    
    with pytest.raises(UserNotFoundException):
        uc.Execute(999, "name", "email")
