"""
Admin API endpoints for CRUD operations on films, actors, genres and countries.
These endpoints are only accessible to superusers.
"""

from fastapi import APIRouter

from .films import router as films_router
from .stuff import router as stuff_router
from .genres import router as genres_router
from .countries import router as countries_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

# Include routers from separate files
router.include_router(films_router)
router.include_router(stuff_router)
router.include_router(genres_router)
router.include_router(countries_router)

__all__ = ["router"]