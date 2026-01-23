from domain.entity.brand import Brand, BrandCreate
from domain.port.brand_repostory import BrandRepository


class UpdateBrandUseCase:
    def __init__(self, brand_repo: BrandRepository):
        self._brand_repo = brand_repo
    
    def Execute(self, brand_id: int, brand_create: BrandCreate) -> Brand:
        return self._brand_repo.update_brand(brand_id, brand_create)
