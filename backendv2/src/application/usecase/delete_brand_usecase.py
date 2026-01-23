from domain.port.brand_repostory import BrandRepository


class DeleteBrandUseCase:
    def __init__(self, brand_repo: BrandRepository):
        self._brand_repo = brand_repo
    
    def Execute(self, brand_id: int) -> None:
        self._brand_repo.delete_brand(brand_id)
