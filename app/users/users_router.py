from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache


from app.base.email_utils import create_url_for_confirm
from app.auth.dependencies import get_current_user
from app.files.file_dao import FileDAO
from app.lessons.manage.stats_dao import StatsDAO
from app.users.profile_dao import ProfileDAO
from app.users.schemas import SProfile, SUserProfile
from app.database.models.user import User
from app.tasks.tasks import send_user_email
from app.exceptions.http_exceptions import (
    http_exc_400_email_confirm
)


router = APIRouter(
    prefix="/user",
    tags=["Управление пользователями"]
)


@router.get("/get_user_info")
@cache(expire=45)
async def get_user_info(user: User = Depends(get_current_user)):
    profile = await ProfileDAO.find_one_or_none(user_data=user[0].id)
    if not profile:
        return SUserProfile(
            id=user[0].id,
            email=user[0].email,
            register_date=user[0].register_date,
            login=user[0].login,
            role=user[0].role,
            is_verified=user[0].is_verified,
            first_name=None,
            last_name=None,
            profile_pic=None,
            points=0,
            status=None
        )
    else:
        profile_pic = await FileDAO.find_one_or_none(
            user_id=user[0].id,
            file_type=1
        )
        if profile_pic is not None:
            profile_pic = profile_pic[0].file_name

        points = await StatsDAO.get_field_sum(
            StatsDAO.model.earned_points,
            user_id=user[0].id)

        if points is None:
            points = 0

        return SUserProfile(
            id=user[0].id,
            email=user[0].email,
            register_date=user[0].register_date,
            login=user[0].login,
            role=user[0].role,
            is_verified=user[0].is_verified,
            first_name=profile[0].first_name,
            last_name=profile[0].last_name,
            profile_pic=profile_pic,
            points=points,
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
            status=data.status
        )
        return f"id {user[0].id} profile created successfuly"
    else:
        answer = await ProfileDAO.update_user_profile(
            user_id=user[0].id,
            first_name=data.first_name,
            last_name=data.last_name,
            status=data.status
        )
        return f"id {answer} profile updated successfuly"


@router.get("/send_confirm_email")
async def send_confirm_email(user: User = Depends(get_current_user)):
    if user[0].is_verified:
        raise http_exc_400_email_confirm

    profile = await ProfileDAO.find_one_or_none(user_data=user[0].id)

    send_user_email.delay(
        user_email=user[0].email,
        template_name="email_confirm.html",
        user_name=profile[0].first_name,
        url_for_confirm=create_url_for_confirm(
            str(user[0].id)
        )
    )
