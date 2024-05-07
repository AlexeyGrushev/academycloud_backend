from datetime import datetime

from sqlalchemy import Boolean, ForeignKey, func
from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, VARCHAR, CHAR

from app.config.db_settings import Base


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
    login: Mapped[str] = mapped_column(
        VARCHAR(255),
        unique=True,
    )
    hashed_password: Mapped[str] = mapped_column(
        CHAR(255)
    )
    role: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("role.id"),
        default=1
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    is_verified: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )
    register_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        default=func.now()
    )
