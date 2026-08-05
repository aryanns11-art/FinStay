from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base


class Settings(Base):
    """Application settings."""

    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    theme: Mapped[str] = mapped_column(
        String(20),
        default="dark",
    )

    backup_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    auto_backup: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
    )