from app.database.settings import Base
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
        ForeignKey("user.id")
    )
    first_name: Mapped[str] = mapped_column(
        String(50),
    )
    last_name: Mapped[str] = mapped_column(
        String(50),
    )
    profile_picture: Mapped[str] = mapped_column(
        nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(200),
        nullable=True
    )
