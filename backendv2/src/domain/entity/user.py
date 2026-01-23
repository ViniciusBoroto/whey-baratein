from enum import Enum
from pydantic import BaseModel

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

class UserCreate(BaseModel):
    name: str
    email: str
    plain_password: str
    role: UserRole = UserRole.USER

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole = UserRole.USER