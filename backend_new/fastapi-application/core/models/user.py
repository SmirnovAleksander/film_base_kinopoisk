import typing

from fastapi_users.db import (SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase)

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession

class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[int]):
    pass

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, User)