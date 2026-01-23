from domain.entity.user import User, UserCreate
from domain.port.password_hasher import PasswordHasher
from domain.port.user_repository import UserRepository


class UserUseCases:
    def __init__(self, user_repo: UserRepository, password_hasher: PasswordHasher):
        self._user_repo = user_repo
        self._password_hasher = password_hasher
    
    def create(self, user_create: UserCreate) -> User:
        hashed_password = self._password_hasher.hash(user_create.plain_password)
        return self._user_repo.create_user(user_create.name, user_create.email, hashed_password)
    
    def get_by_id(self, user_id: int) -> User:
        return self._user_repo.get_user_by_id(user_id)
    
    def update(self, user_id: int, name: str, email: str) -> User:
        return self._user_repo.update_user(user_id, name, email)
    
    def delete(self, user_id: int) -> None:
        self._user_repo.delete_user(user_id)
