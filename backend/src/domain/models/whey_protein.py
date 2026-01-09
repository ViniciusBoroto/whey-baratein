from pydantic import BaseModel, field_validator
from typing import Dict, Any, Optional


class WheyProtein(BaseModel):
    name: str
    price: float
    brand: str
    serving_size: int
    total_weight: int
    protein_per_serving: int
    reliability: int = 0  # 0-5 stars
    image_url: Optional[str] = None

    #EAAs
    fenilanina: float =0
    histidina: float =0
    isoleucina: float =0
    leucina: float =0
    lisina: float =0
    metionina: float =0
    treonina: float =0
    triptofano: float =0
    valina: float = 0
    
    @field_validator('reliability')
    @classmethod
    def validate_reliability(cls, v):
        if not 0 <= v <= 5:
            raise ValueError('Reliability must be between 0 and 5')
        return v
    
    @field_validator('fenilanina', 'histidina', 'isoleucina', 'leucina', 'lisina', 'metionina', 'treonina', 'triptofano', 'valina', mode='before')
    @classmethod
    def convert_mg_to_g(cls, v, info):
        if v == 0:
            return v
        
        # Get serving size from field values
        serving_size = info.data.get('serving_size', 0) if info.data else 0
        if serving_size == 0:
            return v
        
        # If value seems to be in mg (much larger than serving size), convert to g
        if v > serving_size * 10:  # Heuristic: if EAA value > 10x serving size, likely in mg
            return v / 1000
        return v
    def eea_per_serving(self) -> float:
        return self.fenilanina + self.histidina + self.isoleucina + self.leucina + self.lisina + self.metionina + self.treonina + self.triptofano + self.valina
    def servings_per_packet(self) -> float:
        if self.serving_size == 0:
            return 0
        return self.total_weight / self.serving_size
    def total_eea_per_packet(self) -> float:
        return self.eea_per_serving() * self.servings_per_packet()
    def eea_price(self) -> float:
        total_eea = self.total_eea_per_packet()
        if total_eea == 0:
            return 999999.0  # Use a large number instead of infinity for JSON compatibility
        return self.price / total_eea
    def protein_concentration(self) -> float:
        if self.serving_size == 0:
            return 0
        return (self.protein_per_serving / self.serving_size) * 100


