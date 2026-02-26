from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional


class CountryBase(BaseModel):
    name: str
    iso_code: str
    capital: Optional[str] = None
    region: Optional[str] = None
    subregion: Optional[str] = None
    population: Optional[int] = None
    area: Optional[float] = None
    flag_url: Optional[str] = None

    @field_validator("iso_code")
    @classmethod
    def normalize_iso_code(cls, value: str) -> str:
        """Normaliza el código ISO a mayúsculas y valida su longitud."""
        value = value.strip().upper()
        if len(value) != 3:
            raise ValueError("El código ISO debe tener exactamente 3 caracteres.")
        return value

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("El nombre del país no puede estar vacío.")
        return value.strip()


class CountryCreate(CountryBase):
    """Schema para crear un país (datos provenientes de la API externa)."""
    pass


class CountryResponse(CountryBase):
    """Schema de respuesta con campos generados por la base de datos."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None


class SyncResponse(BaseModel):
    """Respuesta del endpoint de sincronización."""

    inserted: int
    updated: int
    total: int
    message: str
