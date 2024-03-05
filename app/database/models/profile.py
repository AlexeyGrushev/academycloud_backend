from app.database.settings import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, BigInteger, ForeignKey


class Profile(Base):
    __tablename__ = "profile"

    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False
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
    sur_name: Mapped[str] = mapped_column(
        String(50)
    )
    country_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("country.id")
    )
    profile_picture: Mapped[str]
    status: Mapped[str] = mapped_column(
        String(200)
    )
