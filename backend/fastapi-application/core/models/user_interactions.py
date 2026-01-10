from datetime import datetime
from typing import Optional, TYPE_CHECKING
from sqlalchemy import Integer, Text, Float, Boolean, DateTime, ForeignKey, UniqueConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from sqlalchemy.sql import func

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from core.types.user_id import UserIdType

if TYPE_CHECKING:
    from .user import User
    from .film import Film, Series


class Bookmark(Base, IntIdPkMixin):
    """Модель закладок пользователя"""
    __tablename__ = "bookmarks"
    
    user_id: Mapped[UserIdType] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="bookmarks")
    film: Mapped["Film"] = relationship(
        "Film",
        primaryjoin="and_(Film.id==foreign(Bookmark.content_id), Bookmark.content_type=='film')",
        back_populates="bookmarks",
        overlaps="bookmarks"
    )
    series: Mapped["Series"] = relationship(
        "Series",
        primaryjoin="and_(Series.id==foreign(Bookmark.content_id), Bookmark.content_type=='series')",
        back_populates="bookmarks",
        overlaps="bookmarks"
    )
    
    __table_args__ = (
        UniqueConstraint("user_id", "content_id", "content_type", name="uq_bookmark_user_content"),
    )


class Comment(Base, IntIdPkMixin):
    """Модель комментариев к контенту"""
    __tablename__ = "comments"
    
    user_id: Mapped[UserIdType] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    is_edited: Mapped[bool] = mapped_column(Boolean, default=False)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    edited_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="comments")
    film: Mapped["Film"] = relationship(
        "Film",
        primaryjoin="and_(Film.id==foreign(Comment.content_id), Comment.content_type=='film')",
        back_populates="comments",
        overlaps="comments"
    )
    series: Mapped["Series"] = relationship(
        "Series",
        primaryjoin="and_(Series.id==foreign(Comment.content_id), Comment.content_type=='series')",
        back_populates="comments",
        overlaps="comments"
    )


class UserContentRating(Base, IntIdPkMixin):
    """Модель пользовательских рейтингов контента"""
    __tablename__ = "user_ratings"
    
    user_id: Mapped[UserIdType] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)  # 1.0 - 10.0
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now())
    
    # Связи
    user: Mapped["User"] = relationship("User", back_populates="ratings")
    film: Mapped["Film"] = relationship(
        "Film",
        primaryjoin="and_(Film.id==foreign(UserContentRating.content_id), UserContentRating.content_type=='film')",
        back_populates="ratings",
        overlaps="ratings"
    )
    series: Mapped["Series"] = relationship(
        "Series",
        primaryjoin="and_(Series.id==foreign(UserContentRating.content_id), UserContentRating.content_type=='series')",
        back_populates="ratings",
        overlaps="ratings"
    )
    
    __table_args__ = (
        UniqueConstraint("user_id", "content_id", "content_type", name="uq_rating_user_content"),
    )


