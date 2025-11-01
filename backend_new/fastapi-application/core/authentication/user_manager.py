import logging
from typing import Optional, TYPE_CHECKING, Dict, Any
from datetime import datetime
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

    async def on_after_update(
            self,
            user: User,
            update_dict: Dict[str, Any],
            request: Optional["Request"] = None,
    ) -> None:
        """
        Обновляет поле updated_at пользователя после успешного обновления.
        """
        from sqlalchemy import update
        
        # Обновляем поле updated_at текущим временем
        await self.user_db.session.execute(
            update(User)
            .where(User.id == user.id)
            .values(updated_at=datetime.now())
        )
        
        # Коммитим изменения
        await self.user_db.session.commit()
        
        log.warning(f"User {user.id} has been updated. Updated fields: {list(update_dict.keys())}")
