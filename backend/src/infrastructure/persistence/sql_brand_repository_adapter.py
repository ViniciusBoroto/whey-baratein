from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from domain.entity.brand import Brand, BrandCreate, BrandRead
from domain.entity.user import UserRead
from domain.exception.exceptions import BrandNotFoundException, UserNotFoundException
from domain.port.brand_repostory import BrandRepository
from infrastructure.persistence.schemas.schemas import BrandORM


class SqlBrandRepositoryAdapter(BrandRepository):
    def __init__(self, session: Session):
        self._session = session

    def get_brand_by_id(self, brand_id: int) -> BrandRead:
        stmt = select(BrandORM).outerjoin(BrandORM.owner).where(BrandORM.id == brand_id)
        brand = self._session.execute(stmt).scalars().first()
        if brand is None:
            raise BrandNotFoundException(brand_id)
        return self._to_read(brand)

    def create_brand(self, brand_create: BrandCreate) -> Brand:
        brand_orm = BrandORM(**brand_create.model_dump())
        self._session.add(brand_orm)
        try:
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            if 'owner_id' in str(e.orig) and brand_create.owner_id is not None:
                raise UserNotFoundException(brand_create.owner_id)
            raise
        self._session.refresh(brand_orm)
        return self._to_brand(brand_orm)

    def update_brand(self, brand_id: int, brand_create: BrandCreate) -> Brand:
        brand = self._session.get(BrandORM, brand_id)
        if brand is None:
            raise BrandNotFoundException(brand_id)
        
        for key, value in brand_create.model_dump().items():
            setattr(brand, key, value)
        
        try:
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            if 'owner_id' in str(e.orig) and brand_create.owner_id is not None:
                raise UserNotFoundException(brand_create.owner_id)
            raise
        self._session.refresh(brand)
        return self._to_brand(brand)

    def delete_brand(self, brand_id: int) -> None:
        brand = self._session.get(BrandORM, brand_id)
        if brand is None:
            raise BrandNotFoundException(brand_id)
        self._session.delete(brand)
        self._session.commit()

    def _to_brand(self, brand_orm: BrandORM) -> Brand:
        return Brand(**{k: v for k, v in brand_orm.__dict__.items() if not k.startswith('_')})
    
    def _to_read(self, brand_orm: BrandORM) -> BrandRead:
        brand_dict = {k: v for k, v in brand_orm.__dict__.items() if not k.startswith('_') and k != 'owner'}
        brand_dict['owner'] = UserRead(**{k: v for k, v in brand_orm.owner.__dict__.items() if not k.startswith('_')}) if brand_orm.owner else None
        return BrandRead(**brand_dict)
