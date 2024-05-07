from sqlalchemy import select, func

from app.database.dbms import DataBaseHelper
from app.database.models import Stats
from app.config.db_settings import async_session


class StatsDAO(DataBaseHelper):
    model = Stats

    @classmethod
    async def get_field_sum(cls, field, **kwargs):
        async with async_session() as session:
            query = select(func.sum(field)).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one()
