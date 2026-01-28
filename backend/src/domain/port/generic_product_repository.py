from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

TCreate = TypeVar('TCreate')
TRead = TypeVar('TRead')


class GenericProductRepository(ABC, Generic[TCreate, TRead]):
    @abstractmethod
    def create(self, product: TCreate) -> TRead:
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: str) -> TRead:
        pass
    
    @abstractmethod
    def update(self, product_id: str, product: TCreate) -> TRead:
        pass
    
    @abstractmethod
    def delete(self, product_id: str) -> None:
        pass
    
    @abstractmethod
    def list_by_owner(self, owner_id: int) -> List[TRead]:
        pass
