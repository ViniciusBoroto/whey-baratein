
from abc import ABC, abstractmethod

from domain.entity.user import UserRead



class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> UserRead:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, name: str, email: str, password: str) -> UserRead:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user_id: int, name: str, email: str) -> UserRead:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        raise NotImplementedError