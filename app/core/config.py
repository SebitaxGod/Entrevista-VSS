from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración centralizada de la aplicación via variables de entorno."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = "postgresql://postgres:postgres@localhost:5432/countries_db"

    # API externa
    rest_countries_url: str = (
        "https://restcountries.com/v3.1/all"
        "?fields=name,cca3,capital,region,subregion,population,area,flags"
    )
    rest_countries_timeout: int = 30

    # App
    app_title: str = "Países API"
    app_description: str = "API que consume REST Países y almacena los datos en PostgreSQL."
    app_version: str = "1.0.0"


settings = Settings()
