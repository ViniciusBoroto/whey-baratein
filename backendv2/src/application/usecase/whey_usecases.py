from application.usecase.product_usecases import ProductUseCases
from domain.entity.whey import WheyRead, WheyCreate, WheyDetails
from domain.port.brand_repostory import BrandRepository
from domain.port.whey_ports import WheyRepository


class WheyUseCases(ProductUseCases[WheyCreate, WheyRead]):
    def __init__(self, brand_repo: BrandRepository, whey_repo: WheyRepository):
        super().__init__(whey_repo, brand_repo)
    
    def create(self, input: WheyCreate) -> WheyDetails:
        result = super().create(input)
        return WheyDetails(**result.__dict__)
    
    def get_by_id(self, whey_id: str) -> WheyDetails:
        result = super().get_by_id(whey_id)
        return WheyDetails(**result.__dict__)
    
    def update(self, whey_id: str, whey_create: WheyCreate) -> WheyDetails:
        result = super().update(whey_id, whey_create)
        return WheyDetails(**result.__dict__)

