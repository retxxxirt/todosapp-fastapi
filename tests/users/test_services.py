import uuid
from datetime import timedelta, datetime

from jose import jwt
from passlib.handlers.pbkdf2 import pbkdf2_sha256

from app.settings import settings
from app.users import services
from app.users.services import JWT_ALGORITHM


def test_encode_password():
    password_hash = services.encode_password("password")

    assert pbkdf2_sha256.verify("password", password_hash)
    assert not pbkdf2_sha256.verify("invalid-password", password_hash)


def test_verify_password():
    password_hash = pbkdf2_sha256.hash("password")

    assert services.verify_password("password", password_hash)
    assert not services.verify_password("invalid-password", password_hash)


def test_encode_jwt_token():
    user_id, expires_in = uuid.uuid4(), timedelta(seconds=10)

    token = services.encode_jwt_token(user_id, expires_in)
    data = jwt.decode(token, settings.secret_key, [JWT_ALGORITHM])

    assert data["sub"] == str(user_id)


def test_decode_jwt_token():
    user_id, expires = uuid.uuid4(), datetime.utcnow() + timedelta(seconds=10)
    token = jwt.encode({"sub": str(user_id), "exp": expires}, settings.secret_key, JWT_ALGORITHM)

    assert services.decode_jwt_token(token) == user_id


def test_decode_jwt_token_invalid():
    assert services.decode_jwt_token("invalid-token") is None


def test_decode_jwt_token_expired():
    user_id, expires = uuid.uuid4(), datetime.utcnow() - timedelta(seconds=10)
    token = jwt.encode({"sub": str(user_id), "exp": expires}, settings.secret_key, JWT_ALGORITHM)

    assert services.decode_jwt_token(token) is None
