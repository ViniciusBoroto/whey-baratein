from domain.entity.brand import Brand, BrandCreate, BrandRead
from domain.port.brand_repostory import BrandRepository


class BrandUseCases:
    def __init__(self, brand_repo: BrandRepository):
        self._brand_repo = brand_repo
    
    def create(self, brand_create: BrandCreate) -> Brand:
        return self._brand_repo.create_brand(brand_create)
    
    def get_by_id(self, brand_id: int) -> BrandRead:
        return self._brand_repo.get_brand_by_id(brand_id)
    
    def update(self, brand_id: int, brand_create: BrandCreate) -> Brand:
        return self._brand_repo.update_brand(brand_id, brand_create)
    
    def delete(self, brand_id: int) -> None:
        self._brand_repo.delete_brand(brand_id)
