from unittest.mock import Mock

import pytest

from application.usecase.get_user_usecase import GetUserUseCase
from domain.entity.user import User
from domain.exception import UserNotFoundException


def test_get_user():
    user = User(id=1, name="name", email="email", password="hashed_password")
    
    mock_user_repo = Mock()
    mock_user_repo.get_user_by_id.return_value = user

    uc = GetUserUseCase(mock_user_repo)
    result = uc.Execute(1)
    
    assert result.id == 1
    assert result.name == "name"
    assert result.email == "email"


def test_get_user_not_found():
    mock_user_repo = Mock()
    mock_user_repo.get_user_by_id.side_effect = UserNotFoundException(999)

    uc = GetUserUseCase(mock_user_repo)
    
    with pytest.raises(UserNotFoundException):
        uc.Execute(999)
