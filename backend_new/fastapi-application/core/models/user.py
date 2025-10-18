import typing

from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from core.types.user_id import UserIdType

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    pass

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)