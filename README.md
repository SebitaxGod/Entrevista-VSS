# 🌍 Countries Dashboard

API REST construida con **FastAPI** que consume datos de [REST Countries API](https://restcountries.com/) y los persiste en **PostgreSQL**. Incluye un dashboard web con tabla interactiva y gráfico de población por región.

## Stack

| Capa | Tecnología |
|------|-----------|
| API | FastAPI + Uvicorn |
| ORM | SQLAlchemy 2.x |
| Schemas | Pydantic v2 |
| Base de datos | PostgreSQL 16 |
| Frontend | HTML + Tailwind CSS + Chart.js |
| API pública | [REST Countries v3.1](https://restcountries.com/) |

---

## Estructura del proyecto

```
app/
├── core/
│   ├── config.py              # Settings centralizados (pydantic-settings)
│   ├── dependencies.py        # Factories de inyección de dependencias FastAPI
│   └── exceptions.py          # Excepciones de dominio personalizadas
├── repositories/
│   ├── abstract_country_repository.py  # Interfaz abstracta
│   └── country_repository.py           # Implementación concreta SQLAlchemy
├── services/
│   ├── country_api_client.py  # Cliente HTTP - REST Countries API
│   └── country_service.py     # Lógica de negocio / orquestación
├── routers/
│   └── countries.py           # Router delgado - solo responsabilidad HTTP
├── database.py                # Engine y sesión SQLAlchemy
├── models.py                  # Modelo ORM Country
├── schemas.py                 # Schemas Pydantic con validadores
└── main.py                    # Punto de entrada FastAPI
static/
├── index.html                 # Estructura HTML + clases Tailwind
└── js/
    ├── api.js                 # Llamadas HTTP a la API
    ├── chart.js               # Renderizado del gráfico
    ├── table.js               # Renderizado y ordenamiento de tabla
    ├── ui.js                  # Toast, stats y formato de números
    └── dashboard.js           # Orquestador: init y binding de eventos
```

---

## Setup

> Requiere [Docker Desktop](https://docs.docker.com/get-docker/) instalado y corriendo.

```bash
# 1. Clonar el repositorio
git clone https://github.com/SebitaxGod/Entrevista-VSS.git
cd Entrevista-VSS

# 2. Levantar base de datos + API
docker compose up --build
```

La API queda disponible en **http://localhost:8000**.

Para detener el proyecto:

```bash
docker compose down
```

---

## Uso

### 1. Abrir el dashboard

Navegar a **http://localhost:8000** y hacer clic en **"Sincronizar datos"** para obtener los ~250 países desde REST Países y guardarlos en la base de datos.

### 2. Endpoints disponibles

| Método | Ruta | Descripción |
|--------|------|-------------|
| `POST` | `/api/countries/sync` | Sincroniza países desde la API externa |
| `GET` | `/api/countries/` | Lista países (filtros: `region`, `search`, `skip`, `limit`) |
| `GET` | `/api/countries/regions` | Regiones únicas |
| `GET` | `/api/countries/{iso_code}` | País por código ISO-3 |

Documentación interactiva: **http://localhost:8000/docs**

### Ejemplos

```bash
# Sincronizar
curl -X POST http://localhost:8000/api/countries/sync

# Listar países de South America
curl "http://localhost:8000/api/countries/?region=South%20America"

# Buscar por nombre
curl "http://localhost:8000/api/countries/?search=argentina"

# Obtener Argentina
curl http://localhost:8000/api/countries/ARG
```

---

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URL de conexión PostgreSQL | `postgresql://postgres:postgres@localhost:5432/countries_db` |