from domain.entity.user import User
from domain.port.user_repository import UserRepository


class GetUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
    
    def Execute(self, user_id: int) -> User:
        return self._user_repo.get_user_by_id(user_id)
