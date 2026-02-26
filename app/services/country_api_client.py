import httpx

from app.core.config import settings
from app.core.exceptions import ExternalAPIError
from app.schemas import CountryCreate


class CountryApiClient:
    """
    Responsabilidad única: consumir la API pública REST Countries
    y transformar la respuesta en objetos de dominio (CountryCreate).
    """

    async def fetch_all(self) -> list[CountryCreate]:
        """Obtiene todos los países desde la API externa y los parsea."""
        raw_data = await self._get_raw_data()
        return self._parse(raw_data)

    async def _get_raw_data(self) -> list[dict]:
        try:
            async with httpx.AsyncClient(timeout=settings.rest_countries_timeout) as client:
                response = await client.get(settings.rest_countries_url)
                response.raise_for_status()
                return response.json()
        except httpx.HTTPStatusError as exc:
            raise ExternalAPIError(
                f"La API externa respondió con error {exc.response.status_code}."
            ) from exc
        except httpx.RequestError as exc:
            raise ExternalAPIError(
                f"No se pudo conectar a la API externa: {exc}"
            ) from exc

    @staticmethod
    def _parse(raw: list[dict]) -> list[CountryCreate]:
        countries: list[CountryCreate] = []
        for item in raw:
            iso_code = item.get("cca3", "").strip()
            if not iso_code:
                continue  # Omitir entradas sin código ISO válido

            capital_list = item.get("capital") or []
            flags = item.get("flags") or {}

            countries.append(
                CountryCreate(
                    name=item.get("name", {}).get("common", "").strip(),
                    iso_code=iso_code,
                    capital=capital_list[0] if capital_list else None,
                    region=item.get("region") or None,
                    subregion=item.get("subregion") or None,
                    population=item.get("population"),
                    area=item.get("area"),
                    flag_url=flags.get("png") or flags.get("svg"),
                )
            )
        return countries
