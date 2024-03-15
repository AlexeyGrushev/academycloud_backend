from typing import Any
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config import settings
from app.exceptions.http_exceptions import http_exc_401_unauthorized


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def is_verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(days=settings.APP_ACCESS_EXPIRE_DAYS)
    to_encode.update(
        {"exp": expire}
    )
    encoded_jwt = jwt.encode(
        to_encode,
        settings.APP_SECRET_KEY,
        settings.APP_ALGORITHM
    )
    return encoded_jwt


def decode_token(token: str) -> dict[str, Any]:
    try:
        decode_jwt = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALGORITHM,
        )
        return decode_jwt

    except JWTError:
        raise http_exc_401_unauthorized
