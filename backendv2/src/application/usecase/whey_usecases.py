import logging
from domain.entity.whey import Whey, WheyCreate, WheyDetails
from domain.port.brand_repostory import BrandRepository
from domain.port.user_repository import UserRepository
from domain.port.whey_ports import WheyRepository


class WheyUseCases:
    def __init__(self, brand_repo: BrandRepository, whey_repo: WheyRepository, user_repo: UserRepository):
        self._brand_repo = brand_repo
        self._whey_repo = whey_repo
        self._user_repo = user_repo
    
    def create(self, input: WheyCreate) -> WheyDetails:
        brand = self._brand_repo.get_brand_by_id(input.brand_id)
        whey = self._whey_repo.create_whey(input)
        logging.info(f"Created whey: {whey}")
        return WheyDetails(brand=brand, **whey.__dict__)
    
    def get_by_id(self, whey_id: str) -> WheyDetails:
        whey = self._whey_repo.get_whey_by_id(whey_id)
        brand = self._brand_repo.get_brand_by_id(whey.brand_id)
        return WheyDetails(brand=brand, **whey.__dict__)
    
    def update(self, whey_id: str, whey_create: WheyCreate) -> WheyDetails:
        brand = self._brand_repo.get_brand_by_id(whey_create.brand_id)
        whey = self._whey_repo.update_whey(whey_id, whey_create)
        return WheyDetails(brand=brand, **whey.__dict__)
    
    def delete(self, whey_id: str) -> None:
        self._whey_repo.delete_whey(whey_id)
