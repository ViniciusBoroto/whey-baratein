
from domain.entity.user import UserCreate, UserRole
from infrastructure.persistence.sql_user_repository_adapter import SqlUserRepositoryAdapter


def test_create_and_retrieve_user(db_session):
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