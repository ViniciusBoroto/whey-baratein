from typing import List, Optional
from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

from domain.entity import brand
from domain.entity.user import UserRole

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    role: Mapped[UserRole] = mapped_column(default=UserRole.USER)

    products: Mapped[List["ProductORM"]] = relationship(back_populates="owner")
    brands: Mapped[List["BrandORM"]] = relationship(back_populates="owner")

class BrandORM(Base):
    __tablename__ = "brands"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    logo_url: Mapped[Optional[str]]
    description: Mapped[Optional[str]]

    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UserORM"] = relationship(back_populates="brands")

    products: Mapped[List["ProductORM"]] = relationship()

class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    image_url: Mapped[Optional[str]]
    type: Mapped[str] 

    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    brand: Mapped["BrandORM"] = relationship(back_populates="products")

    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    owner: Mapped["UserORM"] = relationship(back_populates="products")

    __mapper_args__ = {
    "polymorphic_identity": "product",
    "polymorphic_on": "type",  # You'll need a 'type' column in Product
    }

class WheyORM(ProductORM):
    __tablename__ = "wheys"

    id: Mapped[int] = mapped_column(ForeignKey("products.id"), primary_key=True)

    serving_size: Mapped[int]
    protein_per_serving: Mapped[int]
    total_weight: Mapped[int]

    phenylalanine_mg: Mapped[Optional[int]]
    histidine_mg: Mapped[Optional[int]]
    isoleucine_mg: Mapped[Optional[int]]
    leucine_mg: Mapped[Optional[int]]
    lysine_mg: Mapped[Optional[int]]
    methionine_mg: Mapped[Optional[int]]
    threonine_mg: Mapped[Optional[int]]
    tryptophan_mg: Mapped[Optional[int]]
    valine_mg: Mapped[Optional[int]]

    servings_per_packet: Mapped[float]
    protein_concentration_pct: Mapped[float] 
    eaa_price_per_g: Mapped[Optional[float]] 

    __mapper_args__ = {
    "polymorphic_identity": "whey",
    }

