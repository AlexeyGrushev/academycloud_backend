from app.database.dbms import DataBaseHelper
from app.database.models.profile import Profile

from app.config.db_settings import async_session
from sqlalchemy import (
    update,
)


class ProfileDAO(DataBaseHelper):
    model = Profile

    @classmethod
    async def update_user_profile(
        cls,
        user_id,
        **kwargs
    ):
        async with async_session() as session:
            query = update(cls.model).where(
                cls.model.user_data == user_id
            ).values(
                **kwargs
            ).returning(cls.model.user_data)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one()
