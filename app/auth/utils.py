from typing import Any
from datetime import datetime, timedelta, timezone

from jose import jwt, JWTError
from passlib.context import CryptContext

from app.config.app_settings import settings
from app.users.user_dao import UserDAO
from app.exceptions.http_exceptions import http_exc_401_unauthorized


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def is_verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, exp_days: float) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + \
        timedelta(days=exp_days)
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
            settings.APP_SECRET_KEY,
            settings.APP_ALGORITHM,
        )
        return decode_jwt

    except JWTError:
        raise http_exc_401_unauthorized


async def authenticate_user(login_data: str, password: str):
    user = await UserDAO.find_one_or_none(email=login_data)

    if user is None:
        user = await UserDAO.find_one_or_none(login=login_data)

    if user is None:
        return None

    if is_verify_password(password, str(user[0].hashed_password).strip()):
        return user
    else:
        return None
