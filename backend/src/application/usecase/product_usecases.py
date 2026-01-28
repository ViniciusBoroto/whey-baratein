import logging
from typing import Type, TypeVar, Generic
from domain.port.product_repository import ProductRepository
from domain.entity.product import ProductCreate, ProductRead, ProductDetails

TCreate = TypeVar('TCreate', bound=ProductCreate)
TRead = TypeVar('TRead', bound=ProductRead)
TDetails = TypeVar('TDetails', bound=ProductDetails)


class ProductUseCases(Generic[TCreate, TRead, TDetails]):
    def __init__(
        self, 
        product_repo: ProductRepository[TCreate, TRead, TDetails],
        details_class: Type[TDetails],
        read_class: Type[TRead],
        create_class: Type[TCreate]
    ):
        self._product_repo = product_repo
        self._details_class = details_class
        self._read_class = read_class
        self._create_class = create_class
        
    
    def create(self, product: TCreate) -> TRead:
        created = self._product_repo.create(product)
        logging.info(f"Created {product}")
        return created
    
    def get_by_id(self, product_id: int) -> TDetails:
        product = self._product_repo.get_by_id(product_id)
        return self._details_class(**product.__dict__)
    
    def update(self, product_id: int, product: TCreate) -> TRead:
        updated = self._product_repo.update(product_id, product)
        logging.info(f"Updated {product}")
        return updated
    
    def delete(self, product_id: int) -> None:
        self._product_repo.delete(product_id)
        logging.info(f"Deleted product: {product_id}")
