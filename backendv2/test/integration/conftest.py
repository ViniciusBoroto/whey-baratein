import pytest
from infrastructure.persistence.schemas.schemas import Base, BrandORM, UserORM
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
# from src.models import Base  # Import your SQLAlchemy declarative base

# 1. Spin up the Container (Session Scope = Runs once per test suite)
@pytest.fixture(scope="session")
def postgres_container():
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres

# 2. Create the Engine (Session Scope)
@pytest.fixture(scope="session")
def engine(postgres_container):
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)
    
    # Create tables once
    with engine.begin() as conn:
        Base.metadata.create_all(conn)
        
    yield engine
    
    # Teardown (optional as container handles it, but good practice)
    engine.dispose()

# 3. The Db Session (Function Scope = Runs for every test function)
@pytest.fixture(scope="function")
def db_session(engine):
    """
    Creates a new database session for a test.
    Rolls back the transaction after the test is complete.
    """
    connection = engine.connect()
    transaction = connection.begin()
    
    # Bind the session to this specific connection/transaction
    SessionLocal = sessionmaker(bind=connection)
    session = SessionLocal()

    yield session

    # TEARDOWN: Close session and rollback transaction to keep DB clean
    session.close()
    transaction.rollback()
    connection.close()

@pytest.fixture
def seed_brands(db_session):
    brands = [BrandORM(name="Brand 1"), BrandORM(name="Brand 2"), BrandORM(name="Brand 3")]
    db_session.add_all(brands)
    db_session.flush()
    return brands

@pytest.fixture
def seed_users(db_session):
    users = [UserORM(name="User 1", email="user1@example.com", password="pass1"),
             UserORM(name="User 2", email="user2@example.com", password="pass2"),
             UserORM(name="User 3", email="user3@example.com", password="pass3")]
    db_session.add_all(users)
    db_session.flush()
    return users
