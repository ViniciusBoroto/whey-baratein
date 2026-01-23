from domain.entity.whey import WheyDetails
from domain.port.brand_ports import BrandRepository
from domain.port.whey_ports import WheyRepository


class GetWheyUseCase:
    def __init__(self, brand_repo: BrandRepository, whey_repo: WheyRepository):
        self._brand_repo = brand_repo
        self._whey_repo = whey_repo
        
    def Execute(self, whey_id: str) -> WheyDetails:
        whey = self._whey_repo.get_whey_by_id(whey_id)
        brand = self._brand_repo.get_brand_by_id(whey.brand_id)
        return WheyDetails(brand=brand, **whey.__dict__)
