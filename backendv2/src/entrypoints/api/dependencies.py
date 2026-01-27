from sqlalchemy import Engine, create_engine
from application.usecase.user_usecases import UserUseCases
from application.usecase.whey_usecases import WheyUseCases
from application.usecase.brand_usecases import BrandUseCases
from domain.port.password_hasher import PasswordHasher
from infrastructure.persistence.sql_user_repository_adapter import SqlUserRepositoryAdapter
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from infrastructure.persistence.sql_whey_repository_adapter import SqlWheyRepositoryAdapter
from infrastructure.security import bcrypt_password_hasher

engine = create_engine("sqlite:///./sql_app.db", echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_user_usecases() -> UserUseCases:
    return UserUseCases(SqlUserRepositoryAdapter(SessionLocal()), get_password_hasher())


def get_whey_usecases() -> WheyUseCases:
    return WheyUseCases(SqlWheyRepositoryAdapter(SessionLocal()))

def get_brand_usecases() -> BrandUseCases:
    """
    Dependency injection for BrandUseCases.
    TODO: Implement proper DI with repository instances.
    """
    raise NotImplementedError("Dependency injection not configured")

def get_password_hasher() -> PasswordHasher:
    return bcrypt_password_hasher.BcryptPasswordHasher()
