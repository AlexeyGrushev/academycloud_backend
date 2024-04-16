from fastapi import Depends
from fastapi.routing import APIRouter

from app.auth.dependencies import get_current_user
from app.users.profile_dao import ProfileDAO
from app.users.schemas import SProfile, SUserProfile
from app.users.user_dao import UserDAO
from app.database.models.user import User


router = APIRouter(
    prefix="/user",
    tags=["Управление пользователями"]
)


@router.get("/get_user_info")
async def get_user_info(user: User = Depends(get_current_user)):
    profile = await ProfileDAO.find_one_or_none(user_data=user[0].id)
    if not profile:
        return SUserProfile(
            id=user[0].id,
            email=user[0].email,
            register_date=user[0].register_date,
            login=user[0].login,
            first_name=None,
            last_name=None,
            profile_picture=None,
            status=None
        )
    else:
        return SUserProfile(
            id=user[0].id,
            email=user[0].email,
            register_date=user[0].register_date,
            login=user[0].login,
            first_name=profile[0].first_name,
            last_name=profile[0].last_name,
            profile_picture=profile[0].profile_picture,
            status=profile[0].status
        )


@router.post("/update_profile")
async def update_profile(
        data: SProfile,
        user: User = Depends(get_current_user)):

    profile = await ProfileDAO.find_one_or_none(user_data=user[0].id)

    if not profile:
        await ProfileDAO.insert_values(
            user_data=user[0].id,
            first_name=data.first_name,
            last_name=data.last_name,
            profile_picture=data.profile_picture,
            status=data.status
        )
        return f"id {user[0].id} profile created successfuly"
