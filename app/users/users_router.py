from fastapi import Depends
from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache


from app.base.email_utils import create_url_for_account_activation, create_url_for_confirm, create_url_for_restore
from app.auth.dependencies import get_current_manager, get_current_user
from app.files.file_dao import FileDAO
from app.lessons.manage.stats_dao import StatsDAO
from app.users.profile_dao import ProfileDAO
from app.users.schemas import (
    SProfile,
    SScoreBoardDate,
    SUserActivationManager,
    SUserLoginData,
    SUserProfile,
    SUserUpdate
)
from app.database.models.user import User
from app.tasks.tasks import send_user_email
from app.exceptions.http_exceptions import (
    http_exc_400_email_confirm,
    http_exc_400_bad_data,
    http_exc_403_access_denied,
    http_404_score_not_found
)
from app.users.user_dao import UserDAO
from app.users.utils import update_user


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
            task_completed=0,
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

        task_completed = await StatsDAO.find_all(
            user_id=user[0].id
        )

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
            task_completed=len(task_completed),
            points=points,
            status=profile[0].status
        )


@router.post("/get_user_rating")
async def get_user_rating(
    data: SScoreBoardDate,
    user: User = Depends(get_current_user)
):
    if data.start_date is None and data.end_date is None:
        result = await StatsDAO.get_user_scoreboard_pos(
            user_id=user[0].id
        )
    else:
        result = await StatsDAO.get_user_scoreboard_pos(
            user_id=user[0].id,
            start_date=data.start_date,
            end_date=data.end_date
        )

    if not result:
        raise http_404_score_not_found

    return {
        "user_id": result.user_id,
        "points": result.points,
        "position": result.rank,
        "start_date": data.start_date,
        "end_date": data.end_date
    }


@router.put("/update_user")
async def update_user_endpoint(
    data: SUserUpdate,
    user: User = Depends(get_current_user)
):
    result = await update_user(
        user_id=user[0].id,
        data=data
    )
    return result


@router.put("/update_profile")
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

    return {
        "status": "success, task added"
    }


@router.post("/send_restore_email")
async def send_restore_email(data: SUserLoginData):
    user = await UserDAO.find_one_or_none(login=data.login_data)

    if not user:
        user = await UserDAO.find_one_or_none(email=data.login_data)

    if not user:
        raise http_exc_403_access_denied

    if not user[0].is_verified:
        raise http_exc_403_access_denied

    profile = await ProfileDAO.find_one_or_none(user_data=user[0].id)

    send_user_email.delay(
        user_email=user[0].email,
        template_name="email_restore_password.html",
        user_name=profile[0].first_name,
        url_for_confirm=create_url_for_restore(
            str(user[0].id)
        )
    )

    return {
        "status": "success, task added"
    }


@router.put("/manager_set_user_active")
async def manager_set_user_active(
    data: SUserActivationManager,
    manager: User = Depends(get_current_manager)
):
    user = await UserDAO.find_one_or_none(id=data.id)
    if not user:
        raise http_exc_400_bad_data

    result = await UserDAO.update_user(
        user_id=data.id,
        is_active=data.is_active)

    return {
        "status": "success",
        "id": result,
        "is_active": data.is_active
    }


@router.delete("/deactivate_user")
async def deactivate_account(
        user: User = Depends(get_current_user)):

    result = await UserDAO.update_user(
        user_id=user[0].id,
        is_active=False)

    if user[0].is_verified:
        profile = await ProfileDAO.find_one_or_none(user_data=user[0].id)
        send_user_email.delay(
            user_email=user[0].email,
            template_name="email_restore_account.html",
            user_name=profile[0].first_name,
            url_for_confirm=create_url_for_account_activation(
                str(user[0].id)
            )
        )
    return {
        "status": "success",
        "user_id": user[0].id,
        "info": "User is deactivated"
    }
