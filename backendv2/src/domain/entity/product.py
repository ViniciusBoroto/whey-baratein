from enum import Enum
from typing import Optional
from pydantic import BaseModel, ConfigDict
from domain.entity.brand import Brand

class ProductType(Enum):
    WHEY = "whey"

class ProductCreate(BaseModel):
    name: str
    price: float
    brand_id: Optional[int] = None
    owner_id: Optional[int] = None
    image_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ProductRead(ProductCreate):
    id: int


class ProductDetails(ProductRead):
    brand: Optional[Brand]