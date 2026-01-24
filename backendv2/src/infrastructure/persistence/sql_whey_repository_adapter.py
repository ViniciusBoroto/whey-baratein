from sqlalchemy.orm import Session
from typing import List

from domain.entity.whey import WheyCreate, WheyRead
from domain.exception.exceptions import WheyNotFoundException
from domain.port.generic_product_repository import GenericProductRepository
from infrastructure.persistence.schemas.schemas import WheyORM


class SqlWheyRepositoryAdapter(GenericProductRepository[WheyCreate, WheyRead]):
    def __init__(self, session: Session):
        self._session = session

    def create(self, product: WheyCreate) -> WheyRead:
        whey = WheyORM(**{k: v for k, v in product.model_dump().items() if k not in ['servings_per_packet', 'protein_concentration_pct', 'eaa_price_per_g', 'type']}, type=product.type.value)
        self._session.add(whey)
        self._session.commit()
        self._session.refresh(whey)
        return self._to_read(whey)

    def get_by_id(self, product_id: str) -> WheyRead:
        whey = self._session.get(WheyORM, int(product_id))
        if whey is None:
            raise WheyNotFoundException(product_id)
        return self._to_read(whey)

    def update(self, product_id: str, product: WheyCreate) -> WheyRead:
        whey = self._session.get(WheyORM, int(product_id))
        if whey is None:
            raise WheyNotFoundException(product_id)
        
        for key, value in product.model_dump().items():
            if key not in ['servings_per_packet', 'protein_concentration_pct', 'eaa_price_per_g', 'type']:
                setattr(whey, key, value)
        
        self._session.commit()
        self._session.refresh(whey)
        return self._to_read(whey)

    def delete(self, product_id: str) -> None:
        whey = self._session.get(WheyORM, int(product_id))
        if whey is None:
            raise WheyNotFoundException(product_id)
        self._session.delete(whey)
        self._session.commit()

    def list_by_owner(self, owner_id: int) -> List[WheyRead]:
        wheys = self._session.query(WheyORM).filter(WheyORM.owner_id == owner_id).all()
        return [self._to_read(whey) for whey in wheys]

    def _to_read(self, whey: WheyORM) -> WheyRead:
        return WheyRead(**{k: v for k, v in whey.__dict__.items() if not k.startswith('_')})
