from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.auth.utils import create_hash_password
from app.exceptions.http_exceptions import (
    http_exc_400_bad_email,
    http_exc_400_bad_login
)
from app.auth.schemas import SRegisterUser
from app.users.dao import UserDAO


router = APIRouter(
    prefix="/v1/auth",
    tags=["Аутентификация"]
)


@router.post("/register")
async def create_user(data: SRegisterUser):
    existing_user = await UserDAO.find_one_or_none(email=data.email)
    existing_login = await UserDAO.find_one_or_none(login=data.login)

    if existing_user:
        raise http_exc_400_bad_email

    if existing_login:
        raise http_exc_400_bad_login

    hashed_password = create_hash_password(data.password)

    print(
        "🔴🔴🔴",
        data.email,
        data.phone_number,
        data.login,
        hashed_password
    )

    user = await UserDAO.insert_new_user(
        email=data.email,
        phone=data.phone_number,
        login=data.login,
        hashed_password=hashed_password
    )

    return JSONResponse(
        content={
            "id": user,
            "message": "User was created successfuly"
        },
        status_code=200
    )
