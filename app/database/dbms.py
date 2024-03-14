from app.database.settings import async_session
from sqlalchemy import (
    select,
    insert,
    text,
)


class DataBaseHelper:
    """
        Base class for database manipulations
    """
    model = None

    @classmethod
    async def find_all(cls):
        async with async_session() as session:
            query = select("User")
            result = await session.execute(query)
            return result.fetchall()

    @classmethod
    async def find_one_or_none(cls, *args, **kwargs):
        async with async_session() as session:
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.one_or_none()

    @classmethod
    async def find_max_id(cls, *args, **kwargs):
        async with async_session() as session:
            query = select(cls.model.id).order_by(
                cls.model.id.desc()).limit(1)
            result = await session.execute(query)
            return result

    @classmethod
    async def insert_values(cls, *args, **kwargs):
        async with async_session() as session:
            query = insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()

    @classmethod
    async def get_seq(cls, *args, **kwargs) -> int:
        async with async_session() as session:
            seq = cls.model.__table__.name + "_id_seq"
            query = \
                text(f"select last_value from {seq}")
            result = await session.execute(query)
            return result.fetchone()[0]
