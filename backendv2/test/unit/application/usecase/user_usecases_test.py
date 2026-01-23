from unittest.mock import Mock
import pytest
from application.usecase.user_usecases import UserUseCases
from domain.entity.user import User, UserCreate
from domain.exception import UserNotFoundException


def test_create_user():
    mock_user_repo = Mock()
    mock_password_hasher = Mock()
    mock_password_hasher.hash.return_value = "hashed_password"
    result_user = User(id=1, name="name", email="email", password="hashed_password")
    mock_user_repo.create_user.return_value = result_user

    uc = UserUseCases(mock_user_repo, mock_password_hasher)
    result = uc.create(UserCreate(name="name", email="email", plain_password="plain_password"))

    mock_password_hasher.hash.assert_called_once_with("plain_password")
    assert mock_user_repo.create_user.call_args[0][2] == "hashed_password"
    assert result == result_user


def test_create_user_duplicate_email():
    mock_user_repo = Mock()
    mock_user_repo.create_user.side_effect = Exception("Email already exists")
    mock_password_hasher = Mock()
    mock_password_hasher.hash.return_value = "hashed_password"

    uc = UserUseCases(mock_user_repo, mock_password_hasher)
    
    with pytest.raises(Exception, match="Email already exists"):
        uc.create(UserCreate(name="name", email="duplicate@email.com", plain_password="password"))


def test_get_user():
    user = User(id=1, name="name", email="email", password="hashed_password")
    
    mock_user_repo = Mock()
    mock_user_repo.get_user_by_id.return_value = user

    uc = UserUseCases(mock_user_repo, Mock())
    result = uc.get_by_id(1)
    
    assert result.id == 1
    assert result.name == "name"
    assert result.email == "email"


def test_get_user_not_found():
    mock_user_repo = Mock()
    mock_user_repo.get_user_by_id.side_effect = UserNotFoundException(999)

    uc = UserUseCases(mock_user_repo, Mock())
    
    with pytest.raises(UserNotFoundException):
        uc.get_by_id(999)


def test_update_user():
    updated_user = User(id=1, name="updated_name", email="updated@email.com", password="hashed_password")
    
    mock_user_repo = Mock()
    mock_user_repo.update_user.return_value = updated_user

    uc = UserUseCases(mock_user_repo, Mock())
    result = uc.update(1, "updated_name", "updated@email.com")
    
    assert result.id == 1
    assert result.name == "updated_name"
    assert result.email == "updated@email.com"
    mock_user_repo.update_user.assert_called_once_with(1, "updated_name", "updated@email.com")


def test_update_user_not_found():
    mock_user_repo = Mock()
    mock_user_repo.update_user.side_effect = UserNotFoundException(999)

    uc = UserUseCases(mock_user_repo, Mock())
    
    with pytest.raises(UserNotFoundException):
        uc.update(999, "name", "email")


def test_delete_user():
    mock_user_repo = Mock()
    mock_user_repo.delete_user.return_value = None

    uc = UserUseCases(mock_user_repo, Mock())
    result = uc.delete(1)
    
    assert result is None
    mock_user_repo.delete_user.assert_called_once_with(1)


def test_delete_user_not_found():
    mock_user_repo = Mock()
    mock_user_repo.delete_user.side_effect = UserNotFoundException(999)

    uc = UserUseCases(mock_user_repo, Mock())
    
    with pytest.raises(UserNotFoundException):
        uc.delete(999)
