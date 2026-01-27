from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from application.usecase.user_usecases import UserUseCases
from domain.port.password_hasher import PasswordHasher
from infrastructure.security.jwt_service import create_access_token
from entrypoints.api.dependencies import get_user_usecases, get_password_hasher

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
def login(
    credentials: LoginRequest,
    user_usecases: UserUseCases = Depends(get_user_usecases),
    password_hasher: PasswordHasher = Depends(get_password_hasher)
):
    # TODO: Implement get_by_email in user repository
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Login requires get_by_email implementation in user repository"
    )
