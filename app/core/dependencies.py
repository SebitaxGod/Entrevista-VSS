from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.country_repository import CountryRepository
from app.services.country_api_client import CountryApiClient
from app.services.country_service import CountryService


def get_country_service(db: Session = Depends(get_db)) -> CountryService:
    """Factory de FastAPI que construye el CountryService con sus dependencias inyectadas."""
    repository = CountryRepository(db)
    api_client = CountryApiClient()
    return CountryService(repository=repository, api_client=api_client)
