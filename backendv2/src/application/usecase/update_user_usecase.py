from domain.entity.user import User
from domain.port.user_repository import UserRepository


class UpdateUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
    
    def Execute(self, user_id: int, name: str, email: str) -> User:
        return self._user_repo.update_user(user_id, name, email)
