"""SQLAlchemy models."""

from __future__ import annotations

from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base model class."""


class Router(Base):
    """Router inventory model."""

    __tablename__ = "routers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    site: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    management_ip: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    model: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    os_version: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    uptime_days: Mapped[int] = mapped_column(Integer, nullable=False)
    cpu_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    memory_percent: Mapped[int] = mapped_column(Integer, nullable=False)
    serial_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    config_text: Mapped[str] = mapped_column(Text, nullable=False)

