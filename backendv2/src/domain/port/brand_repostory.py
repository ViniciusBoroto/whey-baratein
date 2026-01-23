from abc import ABC, abstractmethod

from domain.entity import Brand
from domain.entity.brand import BrandCreate


class BrandRepository(ABC):
    @abstractmethod
    def get_brand_by_id(self, brand_id: int) -> Brand:
        raise NotImplementedError

    @abstractmethod
    def create_brand(self, brand_create: BrandCreate) -> Brand:
        raise NotImplementedError

    @abstractmethod
    def update_brand(self, brand_id: int, brand_create: BrandCreate) -> Brand:
        raise NotImplementedError

    @abstractmethod
    def delete_brand(self, brand_id: int) -> None:
        raise NotImplementedError