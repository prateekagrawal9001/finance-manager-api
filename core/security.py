import bcrypt
import jwt
from core.config import settings
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from database.session import get_db
from database.model.revoked_token import RevokedToken
from typing import Optional



def hash_password(plain_password: str) -> str:
    """Hash a plain text password."""
    return bcrypt.hashpw(plain_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain text password against a hashed password."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict):
    """Create a JWT token with the given data."""
    
    to_encode = data.copy()
    # include a unique identifier (jti) for revocation tracking
    jti = to_encode.get("jti") or str(int(datetime.now().timestamp() * 1000))
    to_encode.update({"jti": jti, "alg": settings.JWT_ALGORITHM, "typ": "JWT", "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)})
    encoded_jwt = jwt.encode(to_encode, settings.JWT_TOKEN_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)
    return encoded_jwt


def revoke_token(token: str, db: Optional[Session] = None):
    """Record a token as revoked (store its `jti` and token string)."""
    close_db = False
    if db is None:
        db = get_db().__next__()
        close_db = True
    try:
        try:
            payload = jwt.decode(token, settings.JWT_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options={"verify_exp": False})
        except Exception:
            payload = {}
        jti = payload.get("jti") if payload else None
        if not jti:
            # still store token string with generated jti fallback
            jti = str(int(datetime.now().timestamp() * 1000))
        revoked = RevokedToken(jti=jti, token=token)
        db.add(revoked)
        db.commit()
    finally:
        if close_db:
            db.close()


def is_token_revoked(token: str) -> bool:
    """Return True if token is recorded as revoked."""
    try:
        payload = jwt.decode(token, settings.JWT_TOKEN_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM], options={"verify_exp": False})
    except Exception:
        payload = {}
    jti = payload.get("jti") if payload else None
    if not jti:
        return False
    db = get_db().__next__()
    try:
        exists = db.query(RevokedToken).filter(RevokedToken.jti == jti).first() is not None
        return exists
    finally:
        db.close()


def rotate_access_token(old_token: str, new_data: dict) -> str:
    """Revoke `old_token` and return a newly created access token using `new_data`.

    This is a convenience helper: it revokes the supplied token and issues a new one.
    """
    # revoke old token
    revoke_token(old_token)
    # ensure new_data has fresh jti
    new_token = create_access_token(new_data)
    return new_token