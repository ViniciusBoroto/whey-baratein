from domain.port.user_repository import UserRepository


class DeleteUserUseCase:
    def __init__(self, user_repo: UserRepository):
        self._user_repo = user_repo
    
    def Execute(self, user_id: int) -> None:
        self._user_repo.delete_user(user_id)
