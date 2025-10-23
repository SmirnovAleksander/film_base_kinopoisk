import logging
from typing import Optional, TYPE_CHECKING
from fastapi_users import BaseUserManager, IntegerIDMixin

from core.models import User
from core.config import settings
from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from fastapi import Request

log = logging.getLogger(__name__)

class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    async def on_after_register(
            self,
            user: User,
            request: Optional["Request"] = None
    ):
        log.warning(f"User {user.id} has registered.")

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional["Request"] = None
    ):
        log.warning(f"Verification requested for user {user.id}. Verification token: {token}")

    async def on_after_forgot_password(
            self,
            user: User,
            token: str,
            request: Optional["Request"] = None
    ):
        log.warning(f"User {user.id} has forgot their password. Reset token: {token}")