from datetime import timedelta, datetime
from uuid import UUID

from jose import jwt, JWTError
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app.settings import settings

JWT_ALGORITHM = "HS256"


def encode_password(password: str) -> str:
    """Encode password with pbkdf2_sha256 algo"""
    return pbkdf2_sha256.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    """Verify password by password_hash with pbkdf2_sha256 algo"""
    return pbkdf2_sha256.verify(password, password_hash)


def encode_jwt_token(user_id: UUID, expire_in: timedelta) -> str:
    """Encode jwt token, sub - user_id"""
    data = {"sub": str(user_id), "exp": datetime.utcnow() + expire_in}
    return jwt.encode(data, settings.secret_key, JWT_ALGORITHM)


def decode_jwt_token(token: str) -> UUID | None:
    """Decode jwt token, return None for invalid token"""

    try:
        data = jwt.decode(token, settings.secret_key, JWT_ALGORITHM)
    except JWTError:
        return None

    return UUID(data.get("sub"))
