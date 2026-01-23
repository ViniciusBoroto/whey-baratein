import logging
from domain.entity.brand import Brand
from domain.entity.whey import Whey, WheyCreate, WheyDetails
from domain.port.brand_repostory import BrandRepository
from domain.port.user_repository import UserRepository
from domain.port.whey_repository import WheyRepository


class CreateWheyUseCase:
    def __init__(self, brand_repo: BrandRepository, whey_repo: WheyRepository, user_repo: UserRepository):
        self._brand_repo = brand_repo
        self._whey_repo = whey_repo
        self._user_repo = user_repo
        
    def Execute(self, input: WheyCreate) -> WheyDetails:
        brand = self._brand_repo.get_brand_by_id(input.brand_id)
        user = None
        if input.owner_id is not None:
            user = self._user_repo.get_user_by_id(input.owner_id)
        whey =self._whey_repo.create_whey(input)
        logging.info(f"Created whey: {whey}")
        return WheyDetails(brand=brand,**whey.__dict__)

        