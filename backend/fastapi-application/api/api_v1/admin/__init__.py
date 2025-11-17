"""
Admin API endpoints for CRUD operations on films, actors, genres and countries.
These endpoints are only accessible to superusers.
"""

from fastapi import APIRouter

from .films import router as films_router
from .stuff import router as stuff_router
from .genres import router as genres_router
from .countries import router as countries_router
from .media import router as media_router
from .similar_films import router as similar_films_router
from .film_stills import router as film_stills_router
from .film_watch_providers import router as film_watch_providers_router
from .film_genres import router as film_genres_router
from .film_countries import router as film_countries_router
from .film_stuff import router as film_stuff_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

# Include routers from separate files
router.include_router(films_router)
router.include_router(stuff_router)
router.include_router(genres_router)
router.include_router(countries_router)
router.include_router(media_router)
router.include_router(similar_films_router)
router.include_router(film_stills_router)
router.include_router(film_watch_providers_router)
router.include_router(film_genres_router)
router.include_router(film_countries_router)
router.include_router(film_stuff_router)

__all__ = ["router"]