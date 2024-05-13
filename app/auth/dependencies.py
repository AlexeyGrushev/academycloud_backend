from fastapi import Depends, Request
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.database.models.user import User
from app.exceptions.http_exceptions import (
    http_exc_401_unauthorized,
    http_exc_403_access_denied,
    http_exc_401_banned_user
)
from app.config.app_settings import settings
from app.users.user_dao import UserDAO


def get_token(request: Request):
    token = request.cookies.get("user_access")
    if not token:
        raise http_exc_401_unauthorized
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.APP_SECRET_KEY,
            settings.APP_ALGORITHM
        )
        print(payload)
    except JWTError:
        raise http_exc_401_unauthorized

    expire: str = payload.get("exp")
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise http_exc_401_unauthorized

    user_id: str = payload.get("sub")
    if not user_id:
        raise http_exc_401_unauthorized

    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise http_exc_401_unauthorized

    if user[0].is_active is False:
        try:
            restore: bool = payload.get("restore")
            if restore:
                return user
        except Exception:
            pass
        raise http_exc_401_banned_user

    return user


async def get_current_superuser(user: User = Depends(get_current_user)):
    if user[0].role == settings.APP_SUPERUSER_ROLE_ID:
        return user
    else:
        raise http_exc_403_access_denied


async def get_current_manager(user: User = Depends(get_current_user)):
    if user[0].role == settings.APP_SUPERUSER_ROLE_ID:
        return user
    elif user[0].role == settings.APP_MANAGER_ROLE_ID:
        return user
    else:
        raise http_exc_403_access_denied
