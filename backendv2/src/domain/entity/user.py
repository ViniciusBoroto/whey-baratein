from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    plain_password: str

class User(BaseModel):
    id: int
    name: str
    email: str
    password: str