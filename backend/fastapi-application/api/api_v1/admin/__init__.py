"""
Admin API endpoints for CRUD operations on films, series, stuff, genres and countries.
These endpoints are only accessible to superusers.
"""

from fastapi import APIRouter

from .films import router as films_router
from .series import router as series_router
from .stuff import router as stuff_router
from .genres import router as genres_router
from .countries import router as countries_router
from .similar_content import router as similar_content_router
from .content_images import router as content_images_router
from .content_watch_providers import router as content_watch_providers_router
from .content_genres import router as content_genres_router
from .content_countries import router as content_countries_router
from .content_stuff import router as content_stuff_router
from .users import router as users_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

# Include routers from separate files
router.include_router(films_router)
router.include_router(series_router)
router.include_router(stuff_router)
router.include_router(genres_router)
router.include_router(countries_router)
router.include_router(similar_content_router)
router.include_router(content_images_router)
router.include_router(content_watch_providers_router)
router.include_router(content_genres_router)
router.include_router(content_countries_router)
router.include_router(content_stuff_router)
router.include_router(users_router)

__all__ = ["router"]