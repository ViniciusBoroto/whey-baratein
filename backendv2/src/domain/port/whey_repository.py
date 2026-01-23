from abc import ABC, abstractmethod

from domain.entity.whey import WheyCreate, Whey


class WheyRepository(ABC):
    @abstractmethod
    def create_whey(self, whey_create: WheyCreate) -> Whey:
        raise NotImplementedError

    @abstractmethod
    def get_whey_by_id(self, whey_id: str) -> Whey:
        raise NotImplementedError

    @abstractmethod
    def update_whey(self, whey_id: str, whey_create: WheyCreate) -> Whey:
        raise NotImplementedError

    @abstractmethod
    def delete_whey(self, whey_id: str) -> None:
        raise NotImplementedError
