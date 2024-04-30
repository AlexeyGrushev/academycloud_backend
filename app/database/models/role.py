from app.config.db_settings import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100)
    )
