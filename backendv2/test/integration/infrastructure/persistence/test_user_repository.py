
import pytest
from domain.entity.user import UserCreate, UserRole
from domain.exception.exceptions import UserNotFoundException
from infrastructure.persistence.sql_user_repository_adapter import SqlUserRepositoryAdapter


def test_crud_user(db_session):
    repo = SqlUserRepositoryAdapter(db_session)

    created_user = repo.create("jdoe", "jdoe@example.com", "hashed_password", UserRole.USER)
    db_session.flush()

    fetched_user = repo.get_by_id(created_user.id)
    assert fetched_user is not None
    assert fetched_user.name == "jdoe"
    assert fetched_user.email == "jdoe@example.com"

    updated_user = repo.update(created_user.id, "jdoe_updated", "jdoeupdated@example.com")
    assert updated_user.name == "jdoe_updated"
    assert updated_user.email == "jdoeupdated@example.com"

    fetched_updated_user = repo.get_by_id(created_user.id)
    assert fetched_updated_user is not None
    assert fetched_updated_user.name == "jdoe_updated"
    assert fetched_updated_user.email == "jdoeupdated@example.com"

    repo.delete(created_user.id)
    with pytest.raises(UserNotFoundException):
       repo.get_by_id(created_user.id) 