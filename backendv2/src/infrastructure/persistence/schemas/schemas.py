from typing import Optional
from sqlalchemy import ForeignKey, Computed
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from domain.entity import brand
from domain.entity.user import UserRole

class Base(DeclarativeBase):
    pass

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    role: Mapped[UserRole]

class ProductORM(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    price: Mapped[float]
    brand_id: Mapped[int] = mapped_column(ForeignKey("brands.id"))
    owner_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"))
    image_url: Mapped[Optional[str]]
    type: Mapped[str] 

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

    servings_per_packet: Mapped[float] = mapped_column(Computed("CASE WHEN serving_size = 0 THEN 0 ELSE CAST(total_weight AS FLOAT) / serving_size END"))
    protein_concentration_pct: Mapped[float] = mapped_column(Computed("CASE WHEN serving_size = 0 THEN 0 ELSE (CAST(protein_per_serving AS FLOAT) / serving_size) * 100 END"))
    eaa_price_per_g: Mapped[Optional[float]] = mapped_column(Computed("CASE WHEN (COALESCE(phenylalanine_mg, 0) + COALESCE(histidine_mg, 0) + COALESCE(isoleucine_mg, 0) + COALESCE(leucine_mg, 0) + COALESCE(lysine_mg, 0) + COALESCE(methionine_mg, 0) + COALESCE(threonine_mg, 0) + COALESCE(tryptophan_mg, 0) + COALESCE(valine_mg, 0)) * (CASE WHEN serving_size = 0 THEN 0 ELSE CAST(total_weight AS FLOAT) / serving_size END) / 1000.0 = 0 THEN NULL ELSE price / ((COALESCE(phenylalanine_mg, 0) + COALESCE(histidine_mg, 0) + COALESCE(isoleucine_mg, 0) + COALESCE(leucine_mg, 0) + COALESCE(lysine_mg, 0) + COALESCE(methionine_mg, 0) + COALESCE(threonine_mg, 0) + COALESCE(tryptophan_mg, 0) + COALESCE(valine_mg, 0)) * (CASE WHEN serving_size = 0 THEN 0 ELSE CAST(total_weight AS FLOAT) / serving_size END) / 1000.0) END"))

    __mapper_args__ = {
    "polymorphic_identity": "whey",
    }

