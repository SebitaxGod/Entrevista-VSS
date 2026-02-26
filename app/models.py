from datetime import datetime
from typing import Optional

from sqlalchemy import String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Country(Base):
    """Modelo ORM que representa un país almacenado en la base de datos."""

    __tablename__ = "countries"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    iso_code: Mapped[str] = mapped_column(String(3), unique=True, nullable=False, index=True)
    capital: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    region: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    subregion: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    population: Mapped[Optional[int]] = mapped_column(nullable=True)
    area: Mapped[Optional[float]] = mapped_column(nullable=True)
    flag_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(onupdate=func.now(), nullable=True)
