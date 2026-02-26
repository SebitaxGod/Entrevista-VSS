from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.database import Base, engine
from app.routers import countries


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea las tablas en la BD al iniciar la aplicación si no existen."""
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_title,
    description=settings.app_description,
    version=settings.app_version,
    lifespan=lifespan,
)

app.include_router(countries.router, prefix="/api")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", include_in_schema=False)
def root() -> FileResponse:
    """Sirve el dashboard HTML."""
    return FileResponse("static/index.html")
