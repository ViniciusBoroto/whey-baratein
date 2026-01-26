import pytest
from infrastructure.persistence.schemas.schemas import Base, BrandORM, UserORM
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
# from src.models import Base  # Import your SQLAlchemy declarative base

# 1. Spin up the Container (Function Scope = Runs for each test)
@pytest.fixture(scope="function")
def postgres_container():
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres

# 2. Create the Engine (Function Scope)
@pytest.fixture(scope="function")
def engine(postgres_container):
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)
    
    # Create tables
    Base.metadata.create_all(engine)
        
    yield engine
    
    engine.dispose()

# 3. The Db Session (Function Scope = Runs for every test function)
@pytest.fixture(scope="function")
def db_session(engine):
    """
    Creates a new database session for a test.
    """
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()

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
