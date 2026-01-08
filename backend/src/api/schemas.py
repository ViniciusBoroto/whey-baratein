from pydantic import BaseModel
from typing import Optional

class WheyProteinCreate(BaseModel):
    name: str
    price: float
    brand: str
    serving_size: int
    total_weight: int
    protein_per_serving: int
    fenilanina: float = 0.0
    histidina: float = 0.0
    isoleucina: float = 0.0
    leucina: float = 0.0
    lisina: float = 0.0
    metionina: float = 0.0
    treonina: float = 0.0
    triptofano: float = 0.0
    valina: float = 0.0

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