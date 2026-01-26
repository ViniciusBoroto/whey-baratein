from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List

TCreate = TypeVar('TCreate')
TRead = TypeVar('TRead')
TDetails = TypeVar('TDetails')


class ProductRepository(ABC, Generic[TCreate, TRead, TDetails]):
    @abstractmethod
    def create(self, product: TCreate) -> TRead:
        pass
    
    @abstractmethod
    def get_by_id(self, product_id: int) -> TDetails:
        pass
    
    @abstractmethod
    def update(self, product_id: int, product: TCreate) -> TRead:
        pass
    
    @abstractmethod
    def delete(self, product_id: int) -> None:
        pass
    
    @abstractmethod
    def list_by_owner(self, owner_id: int) -> List[TRead]:
        pass
