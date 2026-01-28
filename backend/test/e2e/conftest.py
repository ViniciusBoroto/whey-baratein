import pytest
from fastapi.testclient import TestClient
from testcontainers.postgres import PostgresContainer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from infrastructure.persistence.schemas.schemas import Base
from entrypoints.api.main import create_app
from entrypoints.api.dependencies import get_user_usecases, get_whey_usecases, get_brand_usecases
from application.usecase.user_usecases import UserUseCases
from application.usecase.whey_usecases import WheyUseCases
from application.usecase.brand_usecases import BrandUseCases
from infrastructure.persistence.sql_user_repository_adapter import SqlUserRepositoryAdapter
from infrastructure.persistence.sql_whey_repository_adapter import SqlWheyRepositoryAdapter
from infrastructure.persistence.sql_brand_repository_adapter import SqlBrandRepositoryAdapter
from infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from infrastructure.security.jwt_service import create_access_token
from domain.entity.user import UserRole

@pytest.fixture(scope="module")
def postgres_container():
    with PostgresContainer("postgres:15-alpine") as postgres:
        yield postgres

@pytest.fixture(scope="module")
def engine(postgres_container):
    db_url = postgres_container.get_connection_url()
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)
    yield engine
    engine.dispose()

@pytest.fixture(scope="module")
def session_factory(engine):
    return sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def client(session_factory):
    app = create_app()
    
    def override_user_usecases():
        return UserUseCases(SqlUserRepositoryAdapter(session_factory()), BcryptPasswordHasher())
    
    def override_whey_usecases():
        return WheyUseCases(SqlWheyRepositoryAdapter(session_factory()))
    
    def override_brand_usecases():
        return BrandUseCases(SqlBrandRepositoryAdapter(session_factory()))
    
    app.dependency_overrides[get_user_usecases] = override_user_usecases
    app.dependency_overrides[get_whey_usecases] = override_whey_usecases
    app.dependency_overrides[get_brand_usecases] = override_brand_usecases
    
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def admin_token():
    return create_access_token(1, "admin@test.com", UserRole.ADMIN)

@pytest.fixture
def user_token():
    return create_access_token(2, "user@test.com", UserRole.USER)
