
from itertools import product
import uuid
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import TypeVar, Generic, List, Type
from domain.entity.product import ProductCreate, ProductDetails, ProductRead
from domain.exception.exceptions import BrandNotFoundException, ProductNotFoundException, UserNotFoundException
from infrastructure.persistence.schemas.schemas import BrandORM, ProductORM

TCreate = TypeVar('TCreate', bound=ProductCreate)
TRead = TypeVar('TRead', bound=ProductRead)
TOrm = TypeVar('TOrm', bound=ProductORM)
TDetails = TypeVar('TDetails', bound=ProductDetails)


class GenericSqlProductRepositoryAdapter(Generic[TOrm,TCreate, TRead, TDetails]):
    orm_class: Type[TOrm]
    create_class: Type[TCreate]
    read_class: Type[TRead]
    details_class: Type[TDetails]
    
    def __init__(self, session: Session, orm_class: Type[TOrm],create_class: Type[TCreate], read_class: Type[TRead], details_class: Type[TDetails]):
        self._session = session
        self.orm_class = orm_class
        self.create_class = create_class
        self.read_class = read_class
        self.details_class = details_class

    def create(self, product: TCreate) -> TRead:
        orm_data = {k: v for k, v in product.model_dump().items() if k != 'type'}
        product_orm = self.orm_class(**orm_data)
        self._session.add(product_orm)
        try:
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            if 'brand_id' in str(e.orig) and product.brand_id is not None:
                raise BrandNotFoundException(product.brand_id)
            if 'owner_id' in str(e.orig) and product.owner_id is not None:
                raise UserNotFoundException(product.owner_id)
            raise
        self._session.refresh(product_orm)
        return self._to_read(product_orm)
    
    def get_by_id(self, product_id: int) -> TDetails:
        stmt = select(self.orm_class).join(self.orm_class.brand)
        product = self._session.execute(stmt).scalars().first()
        if product is None:
            raise ProductNotFoundException(product_id)
        return self._to_details(product)
    
    def update(self, product_id: int, product_create: TCreate) -> TRead:
        fetched_product = self._session.get(self.orm_class, product_id)
        if fetched_product is None:
            raise ProductNotFoundException(product_id)
        
        for key, value in product_create.model_dump().items():
            setattr(fetched_product, key, value)
        
        try:
            self._session.commit()
        except IntegrityError as e:
            self._session.rollback()
            if 'brand_id' in str(e.orig) and product_create.brand_id is not None:
                raise BrandNotFoundException(product_create.brand_id)
            if 'owner_id' in str(e.orig) and product_create.owner_id is not None:
                raise UserNotFoundException(product_create.owner_id)
            raise
        self._session.refresh(fetched_product)
        return self._to_read(fetched_product)
    
    def delete(self, product_id: int) -> None:
        product = self._session.get(self.orm_class, product_id)
        if product is None:
            raise ProductNotFoundException(product_id)
        self._session.delete(product)
        self._session.commit()
    
    def list_by_owner(self, owner_id: int | None) -> List[TDetails]:
        stmt = select(self.orm_class).join(self.orm_class.brand).where(self.orm_class.owner_id == owner_id)
        products = self._session.execute(stmt).scalars().all()
        return [self._to_details(product) for product in products]
    
    def list_all(self, offset: int, limit: int) -> List[TDetails]:
        stmt = select(self.orm_class).join(self.orm_class.brand).offset(offset).limit(limit)
        products = self._session.execute(stmt).scalars().all()
        return [self._to_details(product) for product in products]

    
    def _to_read(self, product_orm: ProductORM) -> TRead:
        return self.read_class(**{k: v for k, v in product_orm.__dict__.items() if not k.startswith('_')})
    def _to_details(self, product_orm: ProductORM) -> TDetails:
        return self.details_class(**{k: v for k, v in product_orm.__dict__.items() if not k.startswith('_')})
