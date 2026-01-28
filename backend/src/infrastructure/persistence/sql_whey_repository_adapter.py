from sqlalchemy.orm import Session
from typing import List

from domain.entity.product import ProductType
from domain.entity.whey import WheyCreate, WheyDetails, WheyRead
from domain.exception.exceptions import WheyNotFoundException
from domain.port.generic_product_repository import GenericProductRepository
from domain.port.whey_ports import WheyRepository
from infrastructure.persistence.generic_sql_product_repository_adapter import GenericSqlProductRepositoryAdapter
from infrastructure.persistence.schemas.schemas import WheyORM

class SqlWheyRepositoryAdapter(GenericSqlProductRepositoryAdapter[WheyORM, WheyCreate, WheyRead, WheyDetails], WheyRepository):
    orm_class = WheyORM
    read_class = WheyRead
    details_class = WheyDetails

    def __init__(self, session: Session):
        super().__init__(session, WheyORM, WheyCreate, WheyRead, WheyDetails, ProductType.WHEY)
