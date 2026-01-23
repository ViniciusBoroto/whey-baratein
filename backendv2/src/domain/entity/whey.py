from pydantic import BaseModel, Field
from typing import Optional

from domain.entity.brand import Brand

class WheyAminoacids(BaseModel):
    phenylalanine_mg: Optional[int] = Field(default=None, description="Fenilanina")
    histidine_mg: Optional[int] = Field(default=None, description="Histidina")
    isoleucine_mg: Optional[int] = Field(default=None, description="Isoleucina")
    leucine_mg: Optional[int] = Field(default=None, description="Leucina")
    lysine_mg: Optional[int] = Field(default=None, description="Lisina")
    methionine_mg: Optional[int] = Field(default=None, description="Metionina")
    threonine_mg: Optional[int] = Field(default=None, description="Treonina")
    tryptophan_mg: Optional[int] = Field(default=None, description="Triptofano")
    valine_mg: Optional[int] = Field(default=None, description="Valina")

class WheyCreate(WheyAminoacids):
    name: str
    price: float
    brand_id: int
    owner_id: Optional[int] 
    
    # Base Specs
    serving_size: int = Field(..., description="Serving size in grams")
    protein_per_serving: int = Field(..., description="Protein content in grams per serving")
    total_weight: int = Field(..., description="Total package weight in grams")
    
    image_url: Optional[str] = None

class Whey(WheyCreate):
    id: str 

    # --- Calculations ---

    def get_total_eaa_mg(self) -> int:
        """Sum of all registered EAAs in mg per serving."""
        # We treat None as 0 for the sum
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

    @property
    def servings_per_packet(self) -> float:
        if self.serving_size == 0: return 0
        return self.total_weight / self.serving_size

    def total_eaa_per_packet_g(self) -> float:
        """Returns total EAAs in the whole packet in GRAMS."""
        total_mg_per_serving = self.get_total_eaa_mg()
        total_mg_packet = total_mg_per_serving * self.servings_per_packet()
        return total_mg_packet / 1000.0  # Convert mg to g

    @property
    def eaa_price_per_g(self) -> Optional[float]:
        """Returns Price per Gram of EAA (Cost Benefit)."""
        total_eaa_g = self.total_eaa_per_packet_g()
        if total_eaa_g == 0:
            return None
        return self.price / total_eaa_g

    @property
    def protein_concentration_pct(self) -> float:
        if self.serving_size == 0: return 0
        return (self.protein_per_serving / self.serving_size) * 100

class WheyDetails(Whey):
    brand: Brand