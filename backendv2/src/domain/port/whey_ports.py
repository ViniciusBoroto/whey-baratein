from domain.port.product_repository import ProductRepository
from domain.entity.whey import WheyCreate, WheyRead


class WheyRepository(ProductRepository[WheyCreate, WheyRead]):
    pass
