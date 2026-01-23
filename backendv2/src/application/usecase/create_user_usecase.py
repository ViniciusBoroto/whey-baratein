from domain.entity.user import User, UserCreate
from domain.port.password_hasher import PasswordHasher
from domain.port.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher):
        self._user_repo = user_repo
        self._password_hasher = password_hasher
    
    def Execute(self, user_create: UserCreate) -> User:
        hashed_password = self._password_hasher.hash(user_create.plain_password)
        return self._user_repo.create_user(user_create.name, user_create.email, hashed_password)
