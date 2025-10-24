import logging
from typing import Optional, TYPE_CHECKING
from fastapi_users import BaseUserManager, IntegerIDMixin
from fastapi_users.db import BaseUserDatabase

from core.models import User
from core.config import settings
from core.types.user_id import UserIdType
from mailing.send_email_confirmed import send_email_confirmed
from mailing.send_verification_email import send_verification_email

if TYPE_CHECKING:
    from fastapi import Request, BackgroundTasks
    from fastapi_users.password import PasswordHelperProtocol

log = logging.getLogger(__name__)

class UserManager(IntegerIDMixin, BaseUserManager[User, UserIdType]):
    reset_password_token_secret = settings.access_token.reset_password_token_secret
    verification_token_secret = settings.access_token.verification_token_secret

    def __init__(
            self,
            user_db: BaseUserDatabase[User, UserIdType],
            password_helper: Optional["PasswordHelperProtocol"] = None,
            background_tasks: Optional["BackgroundTasks"] = None,
    ):
        super().__init__(user_db, password_helper)
        self.background_tasks = background_tasks

    async def on_after_register(
            self,
            user: User,
            request: Optional["Request"] = None
    ):
        log.warning(f"User {user.id} has registered.")
    async def on_after_forgot_password(
            self,
            user: User,
            token: str,
            request: Optional["Request"] = None
    ):
        log.warning(f"User {user.id} has forgot their password. Reset token: {token}")

    async def on_after_request_verify(
            self,
            user: User,
            token: str,
            request: Optional["Request"] = None
    ):
        log.warning(f"Verification requested for user {user.id}. Verification token: {token}")

        verification_link = (
            "http://127.0.0.1:8000/docs#/Auth/verify_verify_api_v1_auth_verify_post"
        )

        self.background_tasks.add_task(
            send_verification_email,
            user=user,
            verification_link=verification_link,
            verification_token=token,
        )

    async def on_after_verify(
            self,
            user: User,
            request: Optional["Request"] = None,
    ):
        log.warning(f"User {user.id} has been verified")

        self.background_tasks.add_task(
            send_email_confirmed,
            user=user
        )
