from pydantic import BaseModel, field_validator
from typing import Optional

class WheyProteinCreate(BaseModel):
    name: str
    price: float
    brand: str
    serving_size: int
    total_weight: int
    protein_per_serving: int
    reliability: int = 0
    image_url: Optional[str] = None
    fenilanina: float = 0.0
    histidina: float = 0.0
    isoleucina: float = 0.0
    leucina: float = 0.0
    lisina: float = 0.0
    metionina: float = 0.0
    treonina: float = 0.0
    triptofano: float = 0.0
    valina: float = 0.0
    
    @field_validator('fenilanina', 'histidina', 'isoleucina', 'leucina', 'lisina', 'metionina', 'treonina', 'triptofano', 'valina', mode='before')
    @classmethod
    def convert_mg_to_g(cls, v, info):
        if v == 0:
            return v
        
        serving_size = info.data.get('serving_size', 0) if info.data else 0
        if serving_size == 0:
            return v
        
        if v > serving_size * 10:
            return v / 1000
        return v
    
    @field_validator('reliability')
    @classmethod
    def validate_reliability(cls, v):
        if not 0 <= v <= 5:
            raise ValueError('Reliability must be between 0 and 5')
        return v

class WheyProteinResponse(WheyProteinCreate):
    id: int
    eea_per_serving: float
    servings_per_packet: float
    total_eea_per_packet: float
    eea_price: float
    protein_concentration: float

    class Config:
        from_attributes = True

class WheyProteinRanking(BaseModel):
    id: int
    name: str
    brand: str
    eea_price: float
    protein_concentration: float
    rank: int