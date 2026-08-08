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

    hotel_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    hotel_address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    phone_number: Mapped[str | None] = mapped_column(String(50), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    gstin: Mapped[str | None] = mapped_column(String(50), nullable=True)
