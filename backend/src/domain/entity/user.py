from enum import Enum
from pydantic import BaseModel, ConfigDict

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

class UserCreate(BaseModel):
    name: str
    email: str
    plain_password: str
    role: UserRole = UserRole.USER

    model_config = ConfigDict(from_attributes=True)

class UserRead(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole = UserRole.USER

    model_config = ConfigDict(from_attributes=True)

class UserWithPassword(UserRead):
    password: str 