from app.database.dbms import DataBaseHelper
from app.database.models.profile import Profile

from app.database.settings import async_session
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
            query = update(cls.model).where(user_data=user_id)
