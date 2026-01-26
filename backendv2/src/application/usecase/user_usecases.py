from domain.entity.user import UserRead, UserCreate
from domain.port.password_hasher import PasswordHasher
from domain.port.user_repository import UserRepository


class UserUseCases:
    def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher):
        self._user_repo = user_repo
        self._password_hasher = password_hasher
    
    def create(self, user_create: UserCreate) -> UserRead:
        hashed_password = self._password_hasher.hash(user_create.plain_password)
        return self._user_repo.create(user_create.name, user_create.email, hashed_password, user_create.role)
    
    def get_by_id(self, user_id: int) -> UserRead:
        return self._user_repo.get_by_id(user_id)
    
    def update(self, user_id: int, name: str, email: str) -> UserRead:
        return self._user_repo.update(user_id, name, email)
    
    def delete(self, user_id: int) -> None:
        self._user_repo.delete(user_id)
