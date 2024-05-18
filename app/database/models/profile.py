from app.config.db_settings import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, ForeignKey


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    user_data: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id"),
        unique=True
    )
    first_name: Mapped[str] = mapped_column(
        String(50),
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
    )
    status: Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )
