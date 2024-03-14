from sqlalchemy import VARCHAR, BigInteger
from app.database.settings import Base
from sqlalchemy.orm import Mapped, mapped_column


class Country(Base):
    __tablename__ = "country"
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    country: Mapped[str] = mapped_column(
        VARCHAR(120),
        unique=True
    )
