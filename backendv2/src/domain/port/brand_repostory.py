from abc import ABC, abstractmethod

from domain.entity import Brand


class BrandRepository(ABC):
    @abstractmethod
    def get_brand_by_id(self, brand_id: int) -> Brand:
        raise NotImplementedError