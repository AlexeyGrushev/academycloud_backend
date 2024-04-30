from app.config.db_settings import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, ForeignKey


class Classroom(Base):
    __tablename__ = "classroom"

    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(50)
    )
    owner: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id"),
        unique=True,
    )
