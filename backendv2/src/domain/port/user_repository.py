
from abc import ABC, abstractmethod

from domain.entity.user import UserRead, UserRole



class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, user_id: int) -> UserRead:
        raise NotImplementedError

    @abstractmethod
    def create(self, name: str, email: str, password: str, role: UserRole = UserRole.USER) -> UserRead:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_id: int, name: str, email: str) -> UserRead:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> None:
        raise NotImplementedError