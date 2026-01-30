from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import jwt
from jwt import PyJWTError
from core.config import settings
from typing import Annotated

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def verify_token(token: Annotated[str, Depends(oauth2_scheme)]):
    # Verify JWT token and return decoded payload as dict
    if not token:
        raise PyJWTError("Invalid token")
    token_data = jwt.decode(token, settings.JWT_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    return token_data