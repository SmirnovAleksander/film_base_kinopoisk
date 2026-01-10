import typing
from typing import List, Optional
from datetime import datetime

from fastapi_users.db import SQLAlchemyBaseUserTable
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.orm import relationship, Mapped
from sqlalchemy import String, Column, DateTime
from sqlalchemy.sql import func

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from core.types.user_id import UserIdType

if typing.TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession
    from .user_interactions import Bookmark, Comment, UserContentRating

class User(Base, IntIdPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    # Дополнительные поля пользователя
    username: Mapped[str] = Column(String(100), unique=True, index=True, nullable=False)
    first_name: Mapped[Optional[str]] = Column(String(100), nullable=True)
    last_name: Mapped[Optional[str]] = Column(String(100), nullable=True)
    created_at: Mapped[datetime] = Column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = Column(DateTime, server_default=func.now(), server_onupdate=func.now())

    # Связи с пользовательскими взаимодействиями
    bookmarks: Mapped[List["Bookmark"]] = relationship("Bookmark", back_populates="user")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="user")
    ratings: Mapped[List["UserContentRating"]] = relationship("UserContentRating", back_populates="user")

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)