from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from application.usecase.user_usecases import UserUseCases
from domain.exception.exceptions import InvalidCredentialsException
from domain.port.password_hasher import PasswordHasher
from entrypoints.api.exceptions.auth_exceptions import UnauthorizedException
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
):
    try:
        user = user_usecases.login(credentials.email, credentials.password)
    except InvalidCredentialsException:
        raise UnauthorizedException()
    except: raise
    return TokenResponse(
        access_token=create_access_token(user.id, user.email, user.role),
    )

