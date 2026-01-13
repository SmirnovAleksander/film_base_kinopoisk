from typing import List, TYPE_CHECKING
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .associations import content_genre

if TYPE_CHECKING:
    from .film import Film
    from .series import Series


class Genre(Base, IntIdPkMixin):
    """Модель жанра"""
    __tablename__ = "genre"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary=content_genre,
        primaryjoin="and_(Genre.id==foreign(content_genre.c.genre_id), content_genre.c.content_type=='film')",
        secondaryjoin="Film.id==foreign(content_genre.c.content_id)",
        back_populates="genres",
        overlaps="series,genres"
    )
    series: Mapped[List["Series"]] = relationship(
        "Series", secondary=content_genre,
        primaryjoin="and_(Genre.id==foreign(content_genre.c.genre_id), content_genre.c.content_type=='series')",
        secondaryjoin="Series.id==foreign(content_genre.c.content_id)",
        back_populates="genres",
        overlaps="films,genres"
    )
