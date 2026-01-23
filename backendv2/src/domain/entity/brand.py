from pydantic import BaseModel
from typing import Optional


class BrandCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None


class Brand(BrandCreate):
    id: int