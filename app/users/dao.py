from app.database.dbms import DataBaseHelper
from app.database.models import User

from app.database.settings import async_session
from sqlalchemy import (
    insert,
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
