from domain.entity.whey import WheyCreate, WheyDetails
from domain.port.brand_ports import BrandRepository
from domain.port.whey_ports import WheyRepository


class UpdateWheyUseCase:
    def __init__(self, brand_repo: BrandRepository, whey_repo: WheyRepository):
        self._brand_repo = brand_repo
        self._whey_repo = whey_repo
        
    def Execute(self, whey_id: str, input: WheyCreate) -> WheyDetails:
        brand = self._brand_repo.get_brand_by_id(input.brand_id)
        whey = self._whey_repo.update_whey(whey_id, input)
        return WheyDetails(brand=brand, **whey.__dict__)
