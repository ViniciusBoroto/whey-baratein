from typing import Optional
from pydantic import BaseModel

from domain.entity.whey import Whey
class CreateWheyInput(BaseModel):
    name: str
    price: float
    brand_id: int
    serving_size: int
    total_weight: int
    protein_per_serving: int
    reliability: int = 0
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


class CreateWheyOutput(BaseModel):
    whey: Whey