import asyncio

from datetime import date, datetime, timedelta, timezone

from app.lessons.manage.stats_dao import StatsDAO


def get_week_dates():
    # Получение текущей даты и времени в UTC
    now = datetime.now(timezone.utc)

    # Вычисление даты начала недели (понедельник)
    start_of_week = now - timedelta(days=now.weekday())

    # Вычисление даты конца недели (воскресенье)
    end_of_week = start_of_week + timedelta(days=6)

    # Возвращение дат начала и конца недели
    return start_of_week.date(), end_of_week.date()


# Вывод дат начала и конца недели
start, end = get_week_dates()
print(f"Начало недели: {start}")
print(f"Конец недели: {end}")


async def test_stats():
    # res = await StatsDAO.get_leaderboard(date(2024, 5, 11), date(2024, 5, 12))
    # res = await StatsDAO.get_user_scoreboard_pos(13)
    res = await StatsDAO.find_all(user_id=14)

    print(res)


asyncio.run(test_stats())
