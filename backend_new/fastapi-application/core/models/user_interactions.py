from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Float, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from .user import User
    from .film import Film


class Bookmark(Base, IntIdPkMixin):
    """Модель закладок пользователя"""
    __tablename__ = "bookmarks"
    
    user_id: Mapped[UserIdType] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("films.id", ondelete="CASCADE"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="bookmarks")
    film: Mapped["Film"] = relationship("Film", back_populates="bookmarks")
    
    __table_args__ = (
        UniqueConstraint("user_id", "film_id", name="uq_bookmark_user_film"),
    )


class Comment(Base, IntIdPkMixin):
    """Модель комментариев к фильмам"""
    __tablename__ = "comments"
    
    user_id: Mapped[UserIdType] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("films.id", ondelete="CASCADE"))
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="comments")
    film: Mapped["Film"] = relationship("Film", back_populates="comments")


class UserFilmRating(Base, IntIdPkMixin):
    """Модель пользовательских рейтингов фильмов"""
    __tablename__ = "user_film_ratings"
    
    user_id: Mapped[UserIdType] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("films.id", ondelete="CASCADE"))
    rating: Mapped[float] = mapped_column(Float, nullable=False)  # 1.0 - 10.0
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="ratings")
    film: Mapped["Film"] = relationship("Film", back_populates="ratings")
    
    __table_args__ = (
        UniqueConstraint("user_id", "film_id", name="uq_rating_user_film"),
    )


class UserFilmHistory(Base, IntIdPkMixin):
    """Модель истории просмотров пользователя"""
    __tablename__ = "user_film_history"
    
    user_id: Mapped[UserIdType] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("films.id", ondelete="CASCADE"))
    visited_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="history")
    film: Mapped["Film"] = relationship("Film", back_populates="history")
    
    __table_args__ = (
        UniqueConstraint("user_id", "film_id", name="uq_history_user_film"),
    )
