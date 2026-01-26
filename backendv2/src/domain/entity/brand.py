from pydantic import BaseModel, ConfigDict
from typing import Optional


class BrandCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class Brand(BrandCreate):
    id: int