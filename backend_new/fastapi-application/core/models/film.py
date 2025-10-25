from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Float, Boolean, DateTime, ForeignKey, ARRAY, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DECIMAL

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user_interactions import Bookmark, Comment, UserFilmRating, UserFilmHistory


class Film(Base, IntIdPkMixin):
    """Модель фильма"""
    __tablename__ = "film"
    
    kinopoisk_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    title: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    original_title: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    full_description: Mapped[Optional[str]] = mapped_column(Text)
    poster: Mapped[Optional[str]] = mapped_column(String(1000))
    year: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    tagline: Mapped[Optional[str]] = mapped_column(Text)
    ru_premiere: Mapped[Optional[str]] = mapped_column(String(100))
    world_premiere: Mapped[Optional[str]] = mapped_column(String(100))
    content_rating: Mapped[Optional[str]] = mapped_column(String(20))
    is_family_friendly: Mapped[bool] = mapped_column(Boolean, default=False)
    duration: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Рейтинги
    rating_kp: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1))
    kp_votes_count: Mapped[Optional[str]] = mapped_column(String(50))
    rating_imdb: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1))
    imdb_votes_count: Mapped[Optional[str]] = mapped_column(String(50))
    user_rating: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1))
    user_rating_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Бюджет и сборы
    budget: Mapped[Optional[str]] = mapped_column(String(100))
    usa_box_office: Mapped[Optional[str]] = mapped_column(String(100))
    rus_box_office: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Связи
    genres: Mapped[List["Genre"]] = relationship(
        "Genre", secondary="film_genre", back_populates="films"
    )
    countries: Mapped[List["Country"]] = relationship(
        "Country", secondary="film_country", back_populates="films"
    )
    stuff: Mapped[List["Stuff"]] = relationship(
        "Stuff", secondary="film_stuff", back_populates="films"
    )
    bookmarks: Mapped[List["Bookmark"]] = relationship("Bookmark", back_populates="film")
    comments: Mapped[List["Comment"]] = relationship("Comment", back_populates="film")
    ratings: Mapped[List["UserFilmRating"]] = relationship("UserFilmRating", back_populates="film")
    history: Mapped[List["UserFilmHistory"]] = relationship("UserFilmHistory", back_populates="film")
    stills: Mapped[List["FilmStill"]] = relationship("FilmStill", back_populates="film")
    watch_providers: Mapped[List["FilmWatchProvider"]] = relationship("FilmWatchProvider", back_populates="film")
    similar_films: Mapped[List["SimilarFilm"]] = relationship("SimilarFilm", back_populates="film")


class Genre(Base, IntIdPkMixin):
    """Модель жанра"""
    __tablename__ = "genre"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary="film_genre", back_populates="genres"
    )


class Country(Base, IntIdPkMixin):
    """Модель страны"""
    __tablename__ = "country"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary="film_country", back_populates="countries"
    )


class Stuff(Base, IntIdPkMixin):
    """Модель участника (актер, режиссер и т.д.)"""
    __tablename__ = "stuff"
    
    kinopoisk_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    name: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    original_name: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    career: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    ganres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    height: Mapped[Optional[str]] = mapped_column(String(50))
    birthday_day_month: Mapped[Optional[str]] = mapped_column(String(50))
    zodiac: Mapped[Optional[str]] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    birthplace: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    spouse: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    children: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    total_films: Mapped[Optional[int]] = mapped_column(Integer)
    career_start_year: Mapped[Optional[int]] = mapped_column(Integer)
    career_end_year: Mapped[Optional[int]] = mapped_column(Integer)
    image: Mapped[Optional[str]] = mapped_column(String(1000))
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary="film_stuff", back_populates="stuff"
    )


class FilmStill(Base, IntIdPkMixin):
    """Модель кадров из фильма"""
    __tablename__ = "film_still"
    
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("film.id", ondelete="CASCADE"), nullable=False)
    picture_id: Mapped[str] = mapped_column(String(20), nullable=False)
    original_url: Mapped[str] = mapped_column(Text, nullable=False)
    source: Mapped[str] = mapped_column(String(16), nullable=False)  # stills, wall
    
    __table_args__ = (
        UniqueConstraint("film_id", "picture_id", "source", name="uq_film_still"),
    )
    
    # Связи
    film: Mapped["Film"] = relationship("Film", back_populates="stills")


class FilmWatchProvider(Base, IntIdPkMixin):
    """Модель провайдеров для просмотра фильма"""
    __tablename__ = "film_watch_provider"
    
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("film.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    url: Mapped[str] = mapped_column(Text, nullable=False)
    logo: Mapped[Optional[str]] = mapped_column(Text)
    
    __table_args__ = (
        UniqueConstraint("film_id", "name", name="uq_film_watch_provider"),
    )
    
    # Связи
    film: Mapped["Film"] = relationship("Film", back_populates="watch_providers")


class SimilarFilm(Base, IntIdPkMixin):
    """Модель похожих фильмов"""
    __tablename__ = "similar_film"
    
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("film.id", ondelete="CASCADE"))
    similar_film_id: Mapped[str] = mapped_column(String(20), nullable=False)  # kinopoisk_id
    similar_film_title: Mapped[str] = mapped_column(String(500), nullable=False)
    similar_film_year: Mapped[Optional[str]] = mapped_column(String(10))
    similar_film_genres: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    similar_film_poster: Mapped[Optional[str]] = mapped_column(Text)
    similar_film_rating: Mapped[Optional[str]] = mapped_column(String(10))
    
    __table_args__ = (
        UniqueConstraint("film_id", "similar_film_id", name="uq_similar_film"),
    )
    
    # Связи
    film: Mapped["Film"] = relationship("Film", back_populates="similar_films")
