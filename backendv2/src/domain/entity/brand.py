from pydantic import BaseModel, ConfigDict
from typing import Optional

from domain.entity.user import UserRead


class BrandCreate(BaseModel):
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None
    owner_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class Brand(BrandCreate):
    id: int

class BrandRead(Brand):
    owner: Optional[UserRead]