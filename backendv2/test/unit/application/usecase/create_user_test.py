from unittest.mock import Mock

from application.usecase.create_user_usecase import CreateUserUseCase
from domain.entity.user import User, UserCreate


def test_create_user():
    mock_user_repo = Mock()
    mock_password_hasher = Mock()
    mock_password_hasher.hash.return_value = "hashed_password"
    result_user = User(id=1, name="name", email="email", password="hashed_password")
    mock_user_repo.create_user.return_value = result_user

    uc = CreateUserUseCase(mock_user_repo, mock_password_hasher)
    result = uc.Execute(UserCreate(name="name", email="email", plain_password="plain_password"))

    mock_password_hasher.hash.assert_called_once_with("plain_password")
    assert mock_user_repo.create_user.call_args[0][2] == "hashed_password"
    assert result == result_user


import pytest
from domain.exception import UserNotFoundException


def test_create_user_duplicate_email():
    mock_user_repo = Mock()
    mock_user_repo.create_user.side_effect = Exception("Email already exists")
    mock_password_hasher = Mock()
    mock_password_hasher.hash.return_value = "hashed_password"

    uc = CreateUserUseCase(mock_user_repo, mock_password_hasher)
    
    with pytest.raises(Exception, match="Email already exists"):
        uc.Execute(UserCreate(name="name", email="duplicate@email.com", plain_password="password"))
