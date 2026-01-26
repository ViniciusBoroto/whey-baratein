from application.usecase.product_usecases import ProductUseCases
from domain.entity.whey import WheyRead, WheyCreate, WheyDetails
from domain.port.brand_repostory import BrandRepository
from domain.port.whey_ports import WheyRepository


class WheyUseCases(ProductUseCases[WheyCreate, WheyRead, WheyDetails]):
    def __init__(self, brand_repo: BrandRepository, whey_repo: WheyRepository):
        super().__init__(whey_repo, brand_repo)

