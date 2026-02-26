from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.core.dependencies import get_country_service
from app.schemas import CountryResponse, SyncResponse
from app.services.country_service import CountryService

router = APIRouter(prefix="/countries", tags=["countries"])


@router.post(
    "/sync",
    response_model=SyncResponse,
    summary="Sincronizar países desde REST Countries API",
)
async def sync_countries(service: CountryService = Depends(get_country_service)):
    """Obtiene todos los países desde restcountries.com y los guarda/actualiza en la BD."""
    return await service.sync()


@router.get(
    "/",
    response_model=list[CountryResponse],
    summary="Listar países",
)
def list_countries(
    region: Optional[str] = Query(None, description="Filtrar por región"),
    search: Optional[str] = Query(None, description="Buscar por nombre o capital"),
    skip: int = Query(0, ge=0, description="Cantidad de registros a omitir"),
    limit: int = Query(50, ge=1, le=250, description="Máximo de resultados a retornar"),
    service: CountryService = Depends(get_country_service),
):
    """Retorna la lista de países almacenados en la base de datos."""
    return service.get_all(region=region, search=search, skip=skip, limit=limit)


@router.get(
    "/regions",
    response_model=list[str],
    summary="Obtener regiones disponibles",
)
def get_regions(service: CountryService = Depends(get_country_service)):
    """Retorna todas las regiones únicas registradas."""
    return service.list_regions()


@router.get(
    "/{iso_code}",
    response_model=CountryResponse,
    summary="Obtener país por código ISO-3",
)
def get_country(iso_code: str, service: CountryService = Depends(get_country_service)):
    """Retorna un país específico por su código ISO-3 (ej: ARG, USA, BRA)."""
    return service.get_by_iso(iso_code)
