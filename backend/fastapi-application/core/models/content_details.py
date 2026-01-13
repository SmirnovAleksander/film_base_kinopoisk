from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, ARRAY, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from sqlalchemy import DECIMAL

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .film import Film
    from .series import Series


class ContentImage(Base, IntIdPkMixin):
    """Модель кадров из контента"""
    __tablename__ = "content_images"
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    picture_id: Mapped[str] = mapped_column(String(20), nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_type: Mapped[str] = mapped_column(String(50), nullable=False) 
    
    __table_args__ = (
        UniqueConstraint("content_id", "content_type", "picture_id", "image_type", name="uq_content_image"),
    )
    
    film: Mapped["Film"] = relationship(
        "Film", 
        primaryjoin="and_(Film.id==foreign(ContentImage.content_id), ContentImage.content_type=='film')",
        back_populates="images",
        overlaps="series,images"
    )
    series: Mapped["Series"] = relationship(
        "Series", 
        primaryjoin="and_(Series.id==foreign(ContentImage.content_id), ContentImage.content_type=='series')",
        back_populates="images",
        overlaps="film,images"
    )


class ContentWatchProvider(Base, IntIdPkMixin):
    """Модель провайдеров для просмотра контента"""
    __tablename__ = "content_watch_provider"
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    provider_name: Mapped[str] = mapped_column(String(200), nullable=False)
    provider_url: Mapped[str] = mapped_column(Text, nullable=False)
    provider_logo: Mapped[Optional[str]] = mapped_column(Text)
    
    __table_args__ = (
        UniqueConstraint("content_id", "content_type", "provider_name", name="uq_content_watch_provider"),
    )
    
    # Связи
    film: Mapped["Film"] = relationship(
        "Film", 
        primaryjoin="and_(Film.id==foreign(ContentWatchProvider.content_id), ContentWatchProvider.content_type=='film')",
        back_populates="watch_providers",
        overlaps="series,watch_providers"
    )
    series: Mapped["Series"] = relationship(
        "Series", 
        primaryjoin="and_(Series.id==foreign(ContentWatchProvider.content_id), ContentWatchProvider.content_type=='series')",
        back_populates="watch_providers",
        overlaps="film,watch_providers"
    )


class SimilarContent(Base, IntIdPkMixin):
    """Модель похожего контента"""
    __tablename__ = "similar_content"
    
    content_id: Mapped[int] = mapped_column(Integer, nullable=False)
    content_type: Mapped[str] = mapped_column(String(20), nullable=False)
    similar_id: Mapped[str] = mapped_column(String(20), nullable=False)  # kinopoisk_id
    similar_type: Mapped[str] = mapped_column(String(20), nullable=False)
    title_ru: Mapped[Optional[str]] = mapped_column(String(500))
    release_year: Mapped[Optional[int]] = mapped_column(Integer)
    genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    poster_url: Mapped[Optional[str]] = mapped_column(Text)
    rating_kp: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1))
    
    __table_args__ = (
        UniqueConstraint("content_id", "content_type", "similar_id", "similar_type", name="uq_similar_content"),
    )
    
    # Связи
    film: Mapped["Film"] = relationship(
        "Film", 
        primaryjoin="and_(Film.id==foreign(SimilarContent.content_id), SimilarContent.content_type=='film')",
        back_populates="similar_content",
        overlaps="series,similar_content"
    )
    series: Mapped["Series"] = relationship(
        "Series", 
        primaryjoin="and_(Series.id==foreign(SimilarContent.content_id), SimilarContent.content_type=='series')",
        back_populates="similar_content",
        overlaps="film,similar_content"
    )
