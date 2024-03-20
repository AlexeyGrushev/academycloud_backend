from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from app.auth.utils import (
    authenticate_user,
    create_access_token,
    create_hash_password
)
from app.exceptions.http_exceptions import (
    http_exc_400_bad_email,
    http_exc_400_bad_login,
    http_exc_401_unauthorized
)
from app.auth.schemas import SLoginUser, SRegisterUser
from app.users.dao import UserDAO


router = APIRouter(
    prefix="/auth",
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

    user = await UserDAO.insert_new_user(
        email=data.email,
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


@router.post("/login")
async def login_user(data: SLoginUser):
    user = await authenticate_user(
        data.login_data,
        data.password
    )

    if not user:
        raise http_exc_401_unauthorized

    access_token = create_access_token({"sub": user[0].id})

    return access_token
