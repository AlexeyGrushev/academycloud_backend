from datetime import date, datetime, timedelta, timezone
from sqlalchemy import select, func, text

from app.database.dbms import DataBaseHelper
from app.database.models import Stats, User
from app.config.db_settings import async_session


class StatsDAO(DataBaseHelper):
    model = Stats

    @classmethod
    async def get_field_sum(cls, field, **kwargs):
        async with async_session() as session:
            query = select(func.sum(field)).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one()

    @classmethod
    async def get_leaderboard(
            cls,
            start_date: date = date(2024, 1, 1),
            end_date: date = datetime.now(
                timezone.utc).date() + timedelta(days=1),
            limit: int = None):
        async with async_session() as session:
            query = select(
                User.id, User.login, User.email, func.sum(
                    cls.model.earned_points).label("points")
            ).join(
                cls.model, User.id == cls.model.user_id
            ).where(
                cls.model.date.between(start_date, end_date),
                User.is_active == True  # noqa
            ).group_by(
                User.id
            ).order_by(
                text("points DESC"),
            ).limit(limit)

            result = await session.execute(query)

            return result.fetchall()

    @classmethod
    async def get_user_scoreboard_pos(
            cls, user_id: int,
            start_date: date = date(2024, 1, 1),
            end_date: date = datetime.now(
                timezone.utc).date() + timedelta(days=1)):
        async with async_session() as session:
            subquery = select(
                cls.model.user_id,
                func.sum(cls.model.earned_points).label("points"),
                func.rank().over(
                    order_by=func.sum(
                        cls.model.earned_points).desc()).label('rank')
            ).where(
                cls.model.date.between(start_date, end_date)
            ).group_by(cls.model.user_id)
            query = select(
                    subquery.c.user_id.label("user_id"),
                    subquery.c.points.label("points"),
                    subquery.c.rank.label("rank")
                ).where(
                subquery.c.user_id == user_id
            )

            result = await session.execute(query)

            return result.one_or_none()
