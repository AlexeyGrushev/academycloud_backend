from datetime import date

from app.database.settings import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, VARCHAR, CHAR


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True
    )
    phone: Mapped[int] = mapped_column(
        BigInteger,
        unique=True
    )
    register_date: Mapped[date]
    login: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        CHAR(255)
    )
