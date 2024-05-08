from sqlalchemy.exc import IntegrityError

from app.auth.utils import create_hash_password
from app.users.schemas import SUserUpdate
from app.users.user_dao import UserDAO


async def update_user(user_id, data: SUserUpdate) -> dict:
    result = {
        "user_id": user_id,
        "updated_email": False,
        "updated_login": False,
        "updated_password": False
    }

    if data.email:
        try:
            await UserDAO.update_user(
                user_id=user_id,
                email=data.email
            )
            await UserDAO.update_user(
                user_id=user_id,
                is_verified=False
            )
            result["updated_email"] = True
        except IntegrityError:
            result["updated_email"] = "Failed. Email exists"
        except Exception:
            result["updated_email"] = "Failed. Unknown error"
    if data.login:
        try:
            await UserDAO.update_user(
                user_id=user_id,
                login=data.login
            )
            result["updated_login"] = True
        except IntegrityError:
            result["updated_login"] = "Failed. Login exists"
        except Exception:
            result["updated_login"] = "Failed. Unknown error"
    if data.password:
        hashed_password = create_hash_password(data.password)
        await UserDAO.update_user(
            user_id=user_id,
            hashed_password=hashed_password
        )
        result["updated_password"] = True

    return result
