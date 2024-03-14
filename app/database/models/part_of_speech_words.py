from sqlalchemy import VARCHAR, BigInteger, ForeignKey
from app.database.settings import Base
from sqlalchemy.orm import Mapped, mapped_column


class Part_of_speech_words(Base):
    __tablename__ = "part_of_speech_words"
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    word: Mapped[str] = mapped_column(
        VARCHAR(100),
        nullable=False,
        unique=True
    )
    part_of_speech_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("part_of_speech.id")
    )
