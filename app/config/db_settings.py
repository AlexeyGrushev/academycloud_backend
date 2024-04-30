from sqlalchemy.ext.asyncio.session import async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine
from app.config.app_settings import settings


engine = create_async_engine(
    settings.DB_URL
)


async_session = async_sessionmaker(
    engine,
    autoflush=False,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    pass
