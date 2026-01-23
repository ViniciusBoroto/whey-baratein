import logging
from typing import TypeVar, Generic
from domain.port.product_repository import ProductRepository
from domain.port.brand_repostory import BrandRepository
from domain.entity.product import ProductCreate, ProductRead, ProductDetails

TCreate = TypeVar('TCreate', bound=ProductCreate)
TRead = TypeVar('TRead', bound=ProductRead)
TDetails = TypeVar('TDetails', bound=ProductDetails)


class ProductUseCases(Generic[TCreate, TRead, TDetails]):
    def __init__(
        self, 
        product_repo: ProductRepository[TCreate, TRead],
        brand_repo: BrandRepository,
        details_class: type[TDetails]
    ):
        self._product_repo = product_repo
        self._brand_repo = brand_repo
        self._details_class = details_class
    
    def create(self, product: TCreate) -> TDetails:
        brand = self._brand_repo.get_brand_by_id(product.brand_id)
        created = self._product_repo.create(product)
        logging.info(f"Created {product.type}: {created.id}")
        return self._details_class(brand=brand, **created.__dict__)
    
    def get_by_id(self, product_id: str) -> TDetails:
        product = self._product_repo.get_by_id(product_id)
        brand = self._brand_repo.get_brand_by_id(product.brand_id)
        return self._details_class(brand=brand, **product.__dict__)
    
    def update(self, product_id: str, product: TCreate) -> TDetails:
        brand = self._brand_repo.get_brand_by_id(product.brand_id)
        updated = self._product_repo.update(product_id, product)
        logging.info(f"Updated {product.type}: {product_id}")
        return self._details_class(brand=brand, **updated.__dict__)
    
    def delete(self, product_id: str) -> None:
        self._product_repo.delete(product_id)
        logging.info(f"Deleted product: {product_id}")
