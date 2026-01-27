from application.usecase.user_usecases import UserUseCases
from application.usecase.whey_usecases import WheyUseCases
from application.usecase.brand_usecases import BrandUseCases
from domain.port.password_hasher import PasswordHasher

def get_user_usecases() -> UserUseCases:
    """
    Dependency injection for UserUseCases.
    TODO: Implement proper DI with repository and password hasher instances.
    """
    raise NotImplementedError("Dependency injection not configured")

def get_whey_usecases() -> WheyUseCases:
    """
    Dependency injection for WheyUseCases.
    TODO: Implement proper DI with repository instances.
    """
    raise NotImplementedError("Dependency injection not configured")

def get_brand_usecases() -> BrandUseCases:
    """
    Dependency injection for BrandUseCases.
    TODO: Implement proper DI with repository instances.
    """
    raise NotImplementedError("Dependency injection not configured")

def get_password_hasher() -> PasswordHasher:
    """
    Dependency injection for PasswordHasher.
    TODO: Implement proper DI with password hasher instance.
    """
    raise NotImplementedError("Dependency injection not configured")
