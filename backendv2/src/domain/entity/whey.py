from pydantic import BaseModel, field_validator
from typing import Dict, Any, Optional

from domain.entity.brand import Brand



class Whey(BaseModel):
    id:int
    name: str
    price: float
    brand: Brand
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
   