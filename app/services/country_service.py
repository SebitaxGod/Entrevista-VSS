from typing import Optional

from app.core.exceptions import CountryNotFoundError
from app.models import Country
from app.repositories.abstract_country_repository import AbstractCountryRepository
from app.schemas import CountryResponse, SyncResponse
from app.services.country_api_client import CountryApiClient


class CountryService:
    """
    Responsabilidad única: orquestar la lógica de negocio relacionada a países.
    """

    def __init__(
        self,
        repository: AbstractCountryRepository,
        api_client: CountryApiClient,
    ) -> None:
        self._repository = repository
        self._api_client = api_client

    async def sync(self) -> SyncResponse:
        """Obtiene países desde la API externa y los persiste en la base de datos."""
        countries = await self._api_client.fetch_all()
        inserted, updated = self._repository.upsert_many(countries)

        return SyncResponse(
            inserted=inserted,
            updated=updated,
            total=inserted + updated,
            message=f"Sincronización completada: {inserted} insertados, {updated} actualizados.",
        )

    def get_all(
        self,
        region: Optional[str],
        search: Optional[str],
        skip: int,
        limit: int,
    ) -> list[Country]:
        return self._repository.get_all(region=region, search=search, skip=skip, limit=limit)

    def list_regions(self) -> list[str]:
        return self._repository.list_regions()

    def get_by_iso(self, iso_code: str) -> Country:
        country = self._repository.get_by_iso(iso_code)
        if not country:
            raise CountryNotFoundError(iso_code)
        return country
