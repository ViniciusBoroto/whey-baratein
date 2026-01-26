from domain.port.product_repository import ProductRepository
from domain.entity.whey import WheyCreate, WheyDetails, WheyRead


class WheyRepository(ProductRepository[WheyCreate, WheyRead, WheyDetails]):
    pass
