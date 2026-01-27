from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from domain.entity.user import UserRole
from infrastructure.config import settings

def create_access_token(user_id: int, email: str, role: UserRole) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role.value,
        "exp": expire
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None
