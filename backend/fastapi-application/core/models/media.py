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
    
    url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True, unique=True)
    title: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True, index=True)
    image_url: Mapped[Optional[str]] = mapped_column(String(1000))
    category: Mapped[Optional[str]] = mapped_column(String(100), index=True)
    publish_date: Mapped[Optional[str]] = mapped_column(String(100))
    card_type: Mapped[Optional[str]] = mapped_column(String(20))
    type: Mapped[Optional[str]] = mapped_column(String(20), default="news", index=True)
    parsed_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
