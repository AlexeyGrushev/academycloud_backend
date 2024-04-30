from app.database.dbms import DataBaseHelper
from app.database.models import User

from app.config.db_settings import async_session
from sqlalchemy import (
    insert,
    update,
)


class UserDAO(DataBaseHelper):
    model = User

    @classmethod
    async def insert_new_user(cls, **kwargs):
        async with async_session() as session:
            query = insert(cls.model).values(**kwargs).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()

    @classmethod
    async def update_user(
        cls,
        user_id,
        **kwargs
    ):
        async with async_session() as session:
            query = update(cls.model).where(
                cls.model.id == user_id
            ).values(
                **kwargs
            ).returning(cls.model.id)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
