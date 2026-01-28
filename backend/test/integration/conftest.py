import pytest
from infrastructure.persistence.schemas.schemas import Base, BrandORM, UserORM
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="session")
def engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def seed_brands(db_session):
    brands = [
        BrandORM(name="Brand 1", logo_url="logo1.png", description="Brand 1 desc"),
        BrandORM(name="Brand 2", logo_url="logo2.png", description="Brand 2 desc"),
        BrandORM(name="Brand 3", logo_url="logo3.png", description="Brand 3 desc")
    ]
    db_session.add_all(brands)
    db_session.commit()
    return brands

@pytest.fixture
def seed_users(db_session):
    from domain.entity.user import UserRole
    users = [
        UserORM(name="User 1", email="user1@example.com", password="pass1", role=UserRole.USER),
        UserORM(name="User 2", email="user2@example.com", password="pass2", role=UserRole.USER),
        UserORM(name="User 3", email="user3@example.com", password="pass3", role=UserRole.ADMIN)
    ]
    db_session.add_all(users)
    db_session.commit()
    return users
