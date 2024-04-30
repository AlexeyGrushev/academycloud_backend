from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, VARCHAR, ForeignKey

from app.config.db_settings import Base


class FileAccounting(Base):
    __tablename__ = "file_accounting"
    id: Mapped[int] = mapped_column(
        BigInteger,
        unique=True,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    file_name: Mapped[int] = mapped_column(
        VARCHAR(255),
        nullable=False
    )
    file_type: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("file_type.id")
    )
    user_id: Mapped[int] = mapped_column(
        BigInteger,
        ForeignKey("user.id")
    )
