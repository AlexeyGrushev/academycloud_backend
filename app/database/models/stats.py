from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, DateTime, ForeignKey, func

from app.config.db_settings import Base


class Stats(Base):
    __tablename__ = "stats"
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id"),
    )
    lesson_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lesson.id")
    )
    earned_points: Mapped[int]
    date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now()
    )
