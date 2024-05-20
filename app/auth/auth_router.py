from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRouter


from app.auth.dependencies import get_current_user
from app.auth.utils import (
    authenticate_user,
    create_access_token,
    create_hash_password,
)
from app.base.email_utils import create_url_for_confirm
from app.base.generate_random_password import generate_password
from app.base.templates import render_template
from app.config.app_settings import settings
from app.exceptions.http_exceptions import (
    http_exc_400_bad_email,
    http_exc_400_bad_login,
    http_exc_401_unauthorized,
    http_exc_401_banned_user
)
from app.auth.schemas import SLoginUser, SRegisterUser
from app.tasks.tasks import send_user_email
from app.users.schemas import SUserUpdate
from app.users.user_dao import UserDAO
from app.users.utils import update_user


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

    send_user_email.delay(
        user_email=data.email,
        template_name="email_confirm.html",
        user_name=data.login,
        url_for_confirm=create_url_for_confirm(
            str(user)
        )
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

    if user[0].is_active is False:
        raise http_exc_401_banned_user

    access_token = create_access_token(
        {"sub": str(user[0].id)},
        settings.APP_ACCESS_EXPIRE_DAYS
    )

    return access_token


@router.get("/confirm_email/{token}", response_class=HTMLResponse)
async def confirm_email(token: str):
    try:
        user = await get_current_user(token)
    except Exception:
        return render_template(
            "confirm_info.html",
            logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
            main_text="404<br><br>"
            "Ссылка, по которой Вы перешли недействительна",
        )

    if user[0].is_verified:
        return render_template(
            "confirm_info.html",
            logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
            main_text="Ваш Email адрес уже подтвержден",
        )

    await UserDAO.update_user(
        user_id=user[0].id,
        is_verified=True
    )

    return render_template(
        "confirm_info.html",
        logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
        main_text=f"Email адрес {user[0].email} успешно подтвержден."
        "<br><br>Вы можете закрыть эту страницу.",
    )


@router.get("/restore_password/{token}", response_class=HTMLResponse)
async def restore_password(token: str):
    try:
        user = await get_current_user(token)
    except Exception:
        return render_template(
            "confirm_info.html",
            logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
            main_text="404<br><br>"
            "Ссылка, по которой Вы перешли недействительна",
        )

    password = generate_password(10)

    result = await update_user(
        user_id=user[0].id,
        data=SUserUpdate(
            email=None,
            login=None,
            password=password
        )
    )

    if result["updated_password"]:

        return render_template(
            "confirm_info.html",
            logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
            main_text=f"Пароль для пользователя {
                user[0].login} успешно сброшен"
            f"<br>Новый пароль: {password}"
            "<br>Скопируйте его прежде чем закрывать страницу!",
        )


@router.get("/activate_account/{token}", response_class=HTMLResponse)
async def activate_account(token: str):
    try:
        user = await get_current_user(token)
    except Exception:
        return render_template(
            "confirm_info.html",
            logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
            main_text="404<br><br>"
            "Ссылка, по которой Вы перешли недействительна",
        )

    if user[0].is_active:
        return render_template(
            "confirm_info.html",
            logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
            main_text="Ваша учётная запись активна"
        )
    else:
        await UserDAO.update_user(
            user_id=user[0].id,
            is_active=True
        )
        return render_template(
            "confirm_info.html",
            logo_path=f"{settings.APP_BASE_URL}/image/logo.png",
            main_text=f"Ваша учётная запись {user[0].login} активирована"
        )
