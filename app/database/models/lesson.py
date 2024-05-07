from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, VARCHAR, ForeignKey

from app.config.db_settings import Base


class Lesson(Base):
    __tablename__ = "lesson"
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    item_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("item.id")
    )
    owner_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id")
    )
    lesson_type: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("lesson_type.id")
    )
    name: Mapped[str] = mapped_column(
        VARCHAR(255)
    )
    reward: Mapped[int]
