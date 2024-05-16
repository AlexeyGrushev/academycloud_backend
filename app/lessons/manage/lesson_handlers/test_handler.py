import math
import json

from app.database.models.lesson import Lesson
from app.lessons.manage.schemas import SLessonAnswer


def distribute_reward(reward, tasks_count):
    # Распределяем награду на задания
    reward_from_task = reward / tasks_count

    # Округляем до ближайшего целого числа
    reward_from_task = math.floor(reward_from_task)

    # Возвращаем награду за задание
    return reward_from_task


def get_lesson(id: int):
    with open(
        f"app/lessons/files/{id}.json",
        "r"
    ) as file:
        lesson_data = json.load(file)
    return lesson_data


def get_lesson_answers(lesson_data) -> list:
    answer_list = []

    for i in lesson_data["body"]["questions"]:
        answer_list.append(i["answer"])

    return answer_list


async def test_lesson_handler(
    data: SLessonAnswer,
    lesson: Lesson
) -> dict:
    lesson_data = get_lesson(lesson[0].id)
    answers = get_lesson_answers(lesson_data)

    if list(data.answer) == list(answers):
        return {
            "correct_answers": [1] * len(answers),
            "reward": int(lesson_data["reward"])
        }
    else:
        right_answers = []
        reward = 0
        reward_for_one_answer = distribute_reward(
            int(lesson_data["reward"]),
            len(answers)
        )

        for i in range(len(data.answer)):
            if data.answer[i] == answers[i]:
                reward += reward_for_one_answer
                right_answers.append(1)
            else:
                right_answers.append(0)

        return {
            "lesson_id": lesson[0].id,
            "correct_answers": right_answers,
            "reward": reward
        }
