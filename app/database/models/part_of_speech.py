from sqlalchemy import VARCHAR, BigInteger
from app.database.settings import Base
from sqlalchemy.orm import Mapped, mapped_column


class Part_of_speech(Base):
    __tablename__ = ""
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False
    )
    