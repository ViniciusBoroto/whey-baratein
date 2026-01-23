
import pytest
from domain.entity.user import UserCreate, UserRole
from domain.exception.exceptions import UserNotFoundException
from infrastructure.persistence.sql_user_repository_adapter import SqlUserRepositoryAdapter


def test_crud_user(db_session):
    # Arrange
    repo = SqlUserRepositoryAdapter(db_session)

    # Act
    # This checks if the create method works and persists data
    created_user =repo.create_user("jdoe", "jdoe@example.com", "hashed_password", UserRole.USER)
    
    # We flush to send SQL to DB, but don't commit (fixture handles rollback)
    db_session.flush() 

    # Assert
    # We try to fetch it back to verify persistence
    fetched_user = repo.get_user_by_id(created_user.id)
    
    assert fetched_user is not None
    assert fetched_user.name == "jdoe"
    assert fetched_user.email == "jdoe@example.com"

    # Update
    updated_user = repo.update_user(created_user.id, "jdoe_updated", "jdoeupdated@example.com")
    assert updated_user.name == "jdoe_updated"
    assert updated_user.email == "jdoeupdated@example.com"

    fetched_updated_user = repo.get_user_by_id(created_user.id)
    
    assert fetched_updated_user is not None
    assert fetched_updated_user.name == "jdoe_updated"
    assert fetched_updated_user.email == "jdoeupdated@example.com"

    # Delete
    repo.delete_user(created_user.id)
    with pytest.raises(UserNotFoundException):
       repo.get_user_by_id(created_user.id) 