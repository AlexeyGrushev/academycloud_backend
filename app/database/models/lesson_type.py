from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, VARCHAR

from app.config.db_settings import Base


class LessonType(Base):
    __tablename__ = "lesson_type"
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    type: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True
    )
