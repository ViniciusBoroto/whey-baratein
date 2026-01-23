from pydantic import BaseModel
from typing import Optional


class Brand(BaseModel):
    id: int
    name: str
    logo_url: Optional[str] = None
    description: Optional[str] = None