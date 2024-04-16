from fastapi import Depends, Request
from jose import jwt, JWTError
from datetime import datetime, timezone

from app.exceptions.http_exceptions import http_exc_401_unauthorized
from app.config import settings
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
    except JWTError:
        raise http_exc_401_unauthorized

    expire: str = payload.get("exp")
    print(expire)
    if (not expire) or (int(expire) < datetime.now(timezone.utc).timestamp()):
        raise http_exc_401_unauthorized

    user_id: str = payload.get("sub")
    if not user_id:
        raise http_exc_401_unauthorized

    user = await UserDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise http_exc_401_unauthorized

    return user
