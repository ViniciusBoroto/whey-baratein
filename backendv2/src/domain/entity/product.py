from typing import Optional
from pydantic import BaseModel
from domain.entity.brand import Brand


class ProductCreate(BaseModel):
    type: str
    name: str
    price: float
    brand_id: int
    owner_id: Optional[int] = None
    image_url: Optional[str] = None


class ProductRead(ProductCreate):
    id: str


class ProductDetails(ProductRead):
    brand: Brand