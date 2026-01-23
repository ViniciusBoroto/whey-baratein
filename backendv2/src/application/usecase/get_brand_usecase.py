from domain.entity.brand import Brand
from domain.port.brand_repostory import BrandRepository


class GetBrandUseCase:
    def __init__(self, brand_repo: BrandRepository):
        self._brand_repo = brand_repo
    
    def Execute(self, brand_id: int) -> Brand:
        return self._brand_repo.get_brand_by_id(brand_id)
