from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer

from core.config import settings
from .auth import router as auth_router
from .users import router as users_router
from .films import router as films_router
from .bookmarks import router as bookmarks_router
from .comments import router as comments_router
from .ratings import router as ratings_router
from .history import router as history_router
from .media import router as media_router
from .stuff import router as stuff_router
from .admin import router as admin_router

http_bearer = HTTPBearer(auto_error=False)

router = APIRouter(
    prefix=settings.api.v1.prefix,
    dependencies=[Depends(http_bearer)],
)

# Аутентификация и пользователи
router.include_router(auth_router)
router.include_router(users_router)

# Основной функционал
router.include_router(films_router)
router.include_router(bookmarks_router)
router.include_router(comments_router)
router.include_router(ratings_router)
router.include_router(history_router)
router.include_router(media_router)
router.include_router(stuff_router)

# Admin функционал (требует аутентификации суперпользователя)
router.include_router(admin_router)