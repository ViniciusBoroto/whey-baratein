from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application.usecase.user_usecases import UserUseCases
from application.usecase.whey_usecases import WheyUseCases
from application.usecase.brand_usecases import BrandUseCases
from domain.port.password_hasher import PasswordHasher
from infrastructure.persistence.sql_user_repository_adapter import SqlUserRepositoryAdapter
from infrastructure.persistence.sql_whey_repository_adapter import SqlWheyRepositoryAdapter
from infrastructure.persistence.sql_brand_repository_adapter import SqlBrandRepositoryAdapter
from infrastructure.security.bcrypt_password_hasher import BcryptPasswordHasher
from infrastructure.config import settings

engine = create_engine(settings.database_url, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_user_usecases() -> UserUseCases:
    return UserUseCases(SqlUserRepositoryAdapter(SessionLocal()), get_password_hasher())


def get_whey_usecases() -> WheyUseCases:
    return WheyUseCases(SqlWheyRepositoryAdapter(SessionLocal()))

def get_brand_usecases() -> BrandUseCases:
    return BrandUseCases(SqlBrandRepositoryAdapter(SessionLocal()))

def get_password_hasher() -> PasswordHasher:
    return BcryptPasswordHasher()
