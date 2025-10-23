from fastapi import APIRouter

from api.dependencies.authentification.backend import auth_backend
from api.api_v1.fastapi_users import fastapi_users
from core.config import settings
from core.schemas.user import UserRead, UserCreate

router = APIRouter(
    prefix=settings.api.v1.auth,
    tags=["Auth"],
)
# /login /logout
router.include_router(
    router = fastapi_users.get_auth_router(auth_backend),
)
# /register
router.include_router(
    router = fastapi_users.get_register_router(UserRead, UserCreate),
)

# /request-verify-token /verify
router.include_router(
    router = fastapi_users.get_verify_router(UserRead),
)

# /forgot-password and /reset-password
router.include_router(
    router = fastapi_users.get_reset_password_router(),
)