import os
import json
import math

from fastapi import UploadFile

from app.database.models.user import User
from app.lessons.manage.item_dao import ItemDAO
from app.lessons.manage.lesson_dao import LessonDAO
from app.lessons.manage.lesson_handlers.test_handler import test_lesson_handler
from app.lessons.manage.lesson_type_dao import LessonTypeDAO
from app.exceptions.http_exceptions import (
    http_400_file_validation,
    http_400_json_parse_exception,
    http_400_bad_lesson_type,
    http_400_item_not_found,
    http_400_bad_lesson_name,
    http_400_bad_lesson_reward,
    http_400_bad_lesson,
    http_400_bad_answer
)
from app.lessons.manage.schemas import SLesson, SLessonAnswer
from app.lessons.manage.stats_dao import StatsDAO
from app.users.user_dao import UserDAO


def distribute_reward(reward, tasks_count):
    # Распределяем награду на задания
    reward_from_task = reward / tasks_count

    # Округляем до ближайшего целого числа
    reward_from_task = math.floor(reward_from_task)

    # Возвращаем награду за задание
    return reward_from_task


async def get_all_items() -> dict:
    """Get all items

    Returns:
        dict: All items
    """
    items = await ItemDAO.find_all()
    result = {}
    for i in items:
        result[i[0].id] = i[0].name
    return result


async def add_new_lesson_logic(user: User, file: UploadFile):

    # Проверяем на соответствие JSON
    if not file.filename.endswith(".json"):
        raise http_400_file_validation
    # - - -

    # Читаем JSON
    try:
        contents = await file.read()
        data = json.loads(contents)
    except Exception:
        raise http_400_json_parse_exception
    # - - -

    # Проверка типа задания и получение его
    lesson_type_id = await LessonTypeDAO.find_one_or_none(type=data["type"])

    if lesson_type_id is None:
        raise http_400_bad_lesson_type
    else:
        lesson_type_id = lesson_type_id[0].id
    # - - -

    # Проверка и получение ID предмета
    try:
        item_id = await ItemDAO.find_one_or_none(id=int(data["item"]))
    except Exception:
        item_id = await ItemDAO.find_one_or_none(
            name=str(data["item"]).capitalize()
        )

    if item_id is None:
        raise http_400_item_not_found
    else:
        item_id = item_id[0].id
    # - - -

    # Проверка не пустого имени и int награды
    if str(data["name"]) == "":
        raise http_400_bad_lesson_name

    try:
        int(data["reward"])
    except Exception:
        raise http_400_bad_lesson_reward
    # - - -

    # Добавление записи о задании в таблицу
    try:
        lesson_id = await LessonDAO.insert_values(
            item_id=item_id,
            owner_id=user[0].id,
            lesson_type=lesson_type_id,
            name=data["name"],
            reward=int(data["reward"])
        )
        record_added = True
    except Exception:
        lesson_id = None
        record_added = False
    # - - -

    # Сохранение JSON файла с заданием
    try:
        with open(
            f"app/lessons/files/{lesson_id}.json",
            "w",
            encoding="UTF-8"
        ) as f:
            json.dump(data, f, ensure_ascii=False)
        file_added = True
    except Exception:
        file_added = False
    # - - -
    return {
        "status": "success",
        "lesson_id": lesson_id,
        "lesson_type_id": lesson_type_id,
        "item_id": item_id,
        "lesson_name": data["name"],
        "reward": data["reward"],
        "db_record_added": record_added,
        "file_downloaded": file_added
    }


async def delete_lesson_logic(data: SLesson):
    lesson = await LessonDAO.find_one_or_none(id=int(data.id))

    if lesson:
        await LessonDAO.delete_values(id=int(data.id))
        record_delete = True
    else:
        record_delete = False

    try:
        os.remove(
            f"app/lessons/files/{str(data.id)}.json"
        )
        file_delete = True
    except Exception:
        file_delete = False

    return {
        "record_delete": record_delete,
        "file_delete": file_delete
    }


async def get_lesson_data(id: int):
    lesson = await LessonDAO.find_one_or_none(id=id)
    if not lesson:
        raise http_400_bad_lesson
    with open(
        f"app/lessons/files/{id}.json",
        "r"
    ) as file:
        lesson_data = json.load(file)
    return lesson_data


async def main_lesson_handler(
    data: SLessonAnswer,
    user: User
):
    lesson = await LessonDAO.find_one_or_none(id=data.id)
    if not lesson:
        raise http_400_bad_lesson
    item_type = await LessonTypeDAO.find_one_or_none(id=lesson[0].lesson_type)
    if not item_type:
        raise http_400_item_not_found
    lesson_data = await get_lesson_data(lesson[0].id)
    if len(lesson_data["body"]["questions"]) != len(data.answer):
        raise http_400_bad_answer

    if item_type[0].type == "test":
        reward_data = await test_lesson_handler(
            data=data,
            lesson=lesson
        )

    await StatsDAO.insert_values(
        user_id=user[0].id,
        lesson_id=lesson[0].id,
        earned_points=reward_data["reward"]
    )

    return reward_data


async def get_lessons_by_item_logic(id: int):
    lessons = await LessonDAO.find_all(item_id=id)
    data_to_return = {}
    for lesson in lessons:
        with open(
            f"app/lessons/files/{lesson[0].id}.json",
            "r"
        ) as file:
            lesson_data = json.load(file)
        lesson_owner = await UserDAO.find_one_or_none(id=lesson[0].owner_id)
        data_to_return[lesson[0].id] = {
            "name": lesson[0].name,
            "owner": lesson_owner[0].login,
            "reward": lesson[0].reward,
            "number_of_questions": len(lesson_data["body"]["questions"])
        }
    return data_to_return
