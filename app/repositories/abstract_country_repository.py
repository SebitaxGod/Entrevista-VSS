from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from app.models import Country
from app.schemas import CountryCreate


class AbstractCountryRepository(ABC):
    """Interfaz abstracta para el repositorio de países."""

    @abstractmethod
    def get_by_iso(self, iso_code: str) -> Optional[Country]:
        ...

    @abstractmethod
    def get_all(
        self,
        region: Optional[str],
        search: Optional[str],
        skip: int,
        limit: int,
    ) -> list[Country]:
        ...

    @abstractmethod
    def list_regions(self) -> list[str]:
        ...

    @abstractmethod
    def upsert_many(self, countries: list[CountryCreate]) -> tuple[int, int]:
        """Inserta o actualiza una lista de países. Retorna (inserted, updated)."""
        ...
