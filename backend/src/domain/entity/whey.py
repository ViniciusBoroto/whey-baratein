from pydantic import Field, computed_field
from typing import Literal, Optional, override

from domain.entity.brand import Brand
from domain.entity.product import ProductCreate, ProductRead, ProductDetails, ProductType


class WheyCreate(ProductCreate):
    type: ProductType = ProductType.WHEY
    serving_size: int = Field(..., description="Serving size in grams")
    protein_per_serving: int = Field(..., description="Protein content in grams per serving")
    total_weight: int = Field(..., description="Total package weight in grams")

    phenylalanine_mg: Optional[int] = Field(default=None, description="Fenilanina")
    histidine_mg: Optional[int] = Field(default=None, description="Histidina")
    isoleucine_mg: Optional[int] = Field(default=None, description="Isoleucina")
    leucine_mg: Optional[int] = Field(default=None, description="Leucina")
    lysine_mg: Optional[int] = Field(default=None, description="Lisina")
    methionine_mg: Optional[int] = Field(default=None, description="Metionina")
    threonine_mg: Optional[int] = Field(default=None, description="Treonina")
    tryptophan_mg: Optional[int] = Field(default=None, description="Triptofano")
    valine_mg: Optional[int] = Field(default=None, description="Valina")

    def get_total_eaa_mg(self) -> int:
        return sum([
            self.phenylalanine_mg or 0,
            self.histidine_mg or 0,
            self.isoleucine_mg or 0,
            self.leucine_mg or 0,
            self.lysine_mg or 0,
            self.methionine_mg or 0,
            self.threonine_mg or 0,
            self.tryptophan_mg or 0,
            self.valine_mg or 0
        ])

    @computed_field
    @property
    def servings_per_packet(self) -> float:
        if self.serving_size == 0: return 0
        return self.total_weight / self.serving_size

    @computed_field
    @property
    def protein_concentration_pct(self) -> float:
        if self.serving_size == 0: return 0
        return (self.protein_per_serving / self.serving_size) * 100

    def total_eaa_per_packet_g(self) -> float:
        total_mg_per_serving = self.get_total_eaa_mg()
        total_mg_packet = total_mg_per_serving * self.servings_per_packet
        return total_mg_packet / 1000.0

    @computed_field
    @property
    def eaa_price_per_g(self) -> Optional[float]:
        total_eaa_g = self.total_eaa_per_packet_g()
        if total_eaa_g == 0:
            return None
        return self.price / total_eaa_g
    

class WheyRead(WheyCreate, ProductRead):
    pass

class WheyDetails(ProductDetails, WheyRead):
    pass