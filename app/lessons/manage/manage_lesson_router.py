from fastapi import Depends, File, UploadFile

from fastapi.routing import APIRouter
from fastapi_cache.decorator import cache

from app.auth.dependencies import get_current_manager, get_current_user
from app.database.models.user import User
from app.lessons.manage.item_dao import ItemDAO
from app.lessons.manage.schemas import SItem, SLesson, SLessonAnswer
from app.exceptions.http_exceptions import (
    http_400_bad_item
)
from app.lessons.manage.utils import (
    add_new_lesson_logic,
    delete_lesson_logic,
    get_all_items,
    get_lesson_data,
    get_lessons_by_item_logic,
    main_lesson_handler
)


router = APIRouter(
    prefix="/lesson",
    tags=["Управление занятиями"]
)


@router.get("/get_items")
@cache(expire=60*60)
async def get_items(user: User = Depends(get_current_user)):
    items = await get_all_items()
    return items


@router.post("/add_item")
async def add_item(data: SItem, user: User = Depends(get_current_manager)):
    item = await ItemDAO.find_one_or_none(name=data.name.capitalize())
    if item:
        raise http_400_bad_item
    result = await ItemDAO.insert_values(name=data.name.capitalize())

    return {
        "status": "success",
        "id": result
    }


@router.post("/add_new_lesson")
async def add_new_lesson(
    user: User = Depends(get_current_manager),
    file: UploadFile = File(...),
):
    result = await add_new_lesson_logic(user, file)

    return result


@router.delete("/delete_lesson")
async def delete_lesson(data: SLesson,
                        user: User = Depends(get_current_manager)
                        ):
    result = await delete_lesson_logic(data)
    return result


@router.get("/get_lesson")
@cache(expire=60*5)
async def get_lesson(lesson_id: int, user: User = Depends(get_current_user)):
    lesson = await get_lesson_data(id=lesson_id)
    return lesson


@router.post("/get_lessons_by_item")
async def get_lessons_by_item(
    data: SLesson,
    user: User = Depends(get_current_user)
):
    result = await get_lessons_by_item_logic(data.id)
    return result


@router.post("/accept_lesson_answer")
async def accept_lesson_answer(
    data: SLessonAnswer,
    user: User = Depends(get_current_user)
):
    result = await main_lesson_handler(
        data=data,
        user=user
    )
    return result
