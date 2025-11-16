"""
Admin API endpoints for CRUD operations on films and actors.
These endpoints are only accessible to superusers.
"""

from fastapi import APIRouter

from .films import router as films_router
from .stuff import router as stuff_router

router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

# Include routers from separate files
router.include_router(films_router)
router.include_router(stuff_router)

__all__ = ["router"]