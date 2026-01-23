from domain.entity.brand import Brand
from domain.entity.whey import Whey, WheyCreate, WheyDetails
from domain.port.brand_ports import BrandRepository
from domain.port.whey_ports import WheyRepository


class CreateWheyUseCase:
    def __init__(self, brand_repo: BrandRepository, whey_repo: WheyRepository):
        self._brand_repo = brand_repo
        self._whey_repo = whey_repo
        
    def Execute(self, input: WheyCreate) -> WheyDetails:
        brand = self._brand_repo.get_brand_by_id(input.brand_id)
        whey =self._whey_repo.create_whey(input)
        return WheyDetails(brand=brand,**whey.__dict__)

        