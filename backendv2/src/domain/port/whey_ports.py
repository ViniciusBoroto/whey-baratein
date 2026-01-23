from abc import ABC, abstractmethod

from domain.entity.whey import WheyCreate, Whey


class WheyRepository(ABC):
    @abstractmethod
    def create_whey(self, whey_create: WheyCreate) -> Whey:
        raise NotImplementedError

    