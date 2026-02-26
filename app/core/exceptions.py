from fastapi import HTTPException, status


class CountryNotFoundError(HTTPException):
    """Excepción de dominio: país no encontrado."""

    def __init__(self, iso_code: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"País con código ISO '{iso_code.upper()}' no encontrado.",
        )


class ExternalAPIError(HTTPException):
    """Error al consumir la API externa de países."""

    def __init__(self, detail: str = "Error al consultar la API externa de países.") -> None:
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=detail,
        )
