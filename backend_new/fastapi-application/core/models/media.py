from datetime import datetime
from typing import Optional
from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class Media(Base, IntIdPkMixin):
    """Модель медиа контента (новости, видео, игры, подкасты)"""
    __tablename__ = "media"
    
    url: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    image: Mapped[Optional[str]] = mapped_column(String(500))
    category: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    comments_count: Mapped[int] = mapped_column(Integer, default=0)
    card_type: Mapped[Optional[str]] = mapped_column(String(50))  # regular, feature
    type: Mapped[Optional[str]] = mapped_column(String(50), index=True)  # news, video, game, podcast
    parsed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
