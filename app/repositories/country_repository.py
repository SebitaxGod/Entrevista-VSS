from typing import Optional

from sqlalchemy.orm import Session

from app.models import Country
from app.schemas import CountryCreate
from app.repositories.abstract_country_repository import AbstractCountryRepository


class CountryRepository(AbstractCountryRepository):
    """Implementación concreta del repositorio de países usando SQLAlchemy."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def get_by_iso(self, iso_code: str) -> Optional[Country]:
        return (
            self._db.query(Country)
            .filter(Country.iso_code == iso_code.upper())
            .first()
        )

    def get_all(
        self,
        region: Optional[str] = None,
        search: Optional[str] = None,
        skip: int = 0,
        limit: int = 50,
    ) -> list[Country]:
        query = self._db.query(Country)

        if region:
            query = query.filter(Country.region.ilike(f"%{region}%"))

        if search:
            term = f"%{search}%"
            query = query.filter(
                Country.name.ilike(term) | Country.capital.ilike(term)
            )

        return query.order_by(Country.name).offset(skip).limit(limit).all()

    def list_regions(self) -> list[str]:
        rows = (
            self._db.query(Country.region)
            .distinct()
            .filter(Country.region.isnot(None))
            .all()
        )
        return sorted(r[0] for r in rows)

    def upsert_many(self, countries: list[CountryCreate]) -> tuple[int, int]:
        """Inserta países nuevos y actualiza los existentes por ISO code."""
        inserted = 0
        updated = 0

        for country_data in countries:
            existing = self.get_by_iso(country_data.iso_code)
            if existing:
                for field, value in country_data.model_dump().items():
                    setattr(existing, field, value)
                updated += 1
            else:
                self._db.add(Country(**country_data.model_dump()))
                inserted += 1

        self._db.commit()
        return inserted, updated
