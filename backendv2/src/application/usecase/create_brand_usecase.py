from domain.entity.brand import Brand, BrandCreate
from domain.port.brand_repostory import BrandRepository


class CreateBrandUseCase:
    def __init__(self, brand_repo: BrandRepository):
        self._brand_repo = brand_repo
    
    def Execute(self, brand_create: BrandCreate) -> Brand:
        return self._brand_repo.create_brand(brand_create)
