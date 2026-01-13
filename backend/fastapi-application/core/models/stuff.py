from typing import List, Optional, TYPE_CHECKING
from sqlalchemy import String, Text, Integer, ARRAY, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from sqlalchemy import DECIMAL

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .associations import content_stuff

if TYPE_CHECKING:
    from .film import Film
    from .series import Series


class Stuff(Base, IntIdPkMixin):
    """Модель участника (актер, режиссер и т.д.)"""
    __tablename__ = "stuff"
    
    kinopoisk_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name_ru: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    name_en: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    career: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    height: Mapped[Optional[str]] = mapped_column(String(50))
    zodiac: Mapped[Optional[str]] = mapped_column(String(50))
    birth_date: Mapped[Optional[str]] = mapped_column(String(100))
    birth_place: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    spouse: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    children: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    films_total: Mapped[Optional[int]] = mapped_column(Integer)
    career_start: Mapped[Optional[int]] = mapped_column(Integer)
    photo_url: Mapped[Optional[str]] = mapped_column(String(1000))
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary=content_stuff,
        primaryjoin="and_(Stuff.id==foreign(content_stuff.c.stuff_id), content_stuff.c.content_type=='film')",
        secondaryjoin="Film.id==foreign(content_stuff.c.content_id)",
        back_populates="stuff",
        overlaps="series,stuff"
    )
    series: Mapped[List["Series"]] = relationship(
        "Series", secondary=content_stuff,
        primaryjoin="and_(Stuff.id==foreign(content_stuff.c.stuff_id), content_stuff.c.content_type=='series')",
        secondaryjoin="Series.id==foreign(content_stuff.c.content_id)",
        back_populates="stuff",
        overlaps="films,stuff"
    )
    images: Mapped[List["StuffImage"]] = relationship("StuffImage", back_populates="stuff", cascade="all, delete-orphan")
    filmography: Mapped[List["StuffFilmography"]] = relationship("StuffFilmography", back_populates="stuff", cascade="all, delete-orphan")


class StuffImage(Base, IntIdPkMixin):
    """Модель изображений персоны"""
    __tablename__ = "stuff_images"
    
    stuff_id: Mapped[int] = mapped_column(Integer, ForeignKey("stuff.id", ondelete="CASCADE"), nullable=False)
    picture_id: Mapped[str] = mapped_column(String(20), nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    image_type: Mapped[str] = mapped_column(String(50), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("stuff_id", "picture_id", "image_type", name="uq_stuff_image"),
    )
    
    stuff: Mapped["Stuff"] = relationship("Stuff", back_populates="images")


class StuffFilmography(Base, IntIdPkMixin):
    """Модель фильмографии персоны"""
    __tablename__ = "stuff_filmography"
    
    stuff_id: Mapped[int] = mapped_column(Integer, ForeignKey("stuff.id", ondelete="CASCADE"), nullable=False)
    content_id: Mapped[str] = mapped_column(String(20), nullable=False)
    title_ru: Mapped[Optional[str]] = mapped_column(String(500))
    title_en: Mapped[Optional[str]] = mapped_column(String(500))
    release_year: Mapped[Optional[int]] = mapped_column(Integer)
    genres: Mapped[Optional[str]] = mapped_column(Text)
    countries: Mapped[Optional[str]] = mapped_column(Text)
    poster_url: Mapped[Optional[str]] = mapped_column(String(1000))
    rating_kp: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1))
    votes_kp: Mapped[Optional[int]] = mapped_column(Integer)
    role: Mapped[Optional[str]] = mapped_column(String(100))
    release_year_start: Mapped[Optional[int]] = mapped_column(Integer)
    release_year_end: Mapped[Optional[int]] = mapped_column(Integer)
    
    __table_args__ = (
        UniqueConstraint("stuff_id", "content_id", "role", name="uq_stuff_filmography"),
    )
    
    stuff: Mapped["Stuff"] = relationship("Stuff", back_populates="filmography")
