from fastapi.routing import APIRouter

from app.user.schemas import User


router = APIRouter(
    prefix="/v1/user",
    tags=["Взаимодействие со своим профилем"]
)


@router.post("/create")
async def create_user(data: User):
    """Создание пользователя

    Returns:
        _type_: _description_
    """
    return data
