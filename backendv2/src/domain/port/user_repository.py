
from abc import ABC, abstractmethod

from domain.entity.user import User



class UserRepository(ABC):
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        raise NotImplementedError

    @abstractmethod
    def create_user(self, name: str, email: str, password: str) -> User:
        raise NotImplementedError