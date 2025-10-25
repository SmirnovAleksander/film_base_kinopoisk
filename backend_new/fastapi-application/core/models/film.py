from datetime import datetime
from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Float, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin

if TYPE_CHECKING:
    from .user_interactions import Bookmark, Comment, UserFilmRating, UserFilmHistory


class Film(Base, IntIdPkMixin):
    """Модель фильма"""
    __tablename__ = "films"
    
    kinopoisk_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(500), nullable=False, index=True)
    original_title: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    description: Mapped[Optional[str]] = mapped_column(Text)
    full_description: Mapped[Optional[str]] = mapped_column(Text)
    poster: Mapped[Optional[str]] = mapped_column(String(500))
    year: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    tagline: Mapped[Optional[str]] = mapped_column(String(500))
    ru_premiere: Mapped[Optional[datetime]] = mapped_column(DateTime)
    world_premiere: Mapped[Optional[datetime]] = mapped_column(DateTime)
    content_rating: Mapped[Optional[str]] = mapped_column(String(10))
    is_family_friendly: Mapped[bool] = mapped_column(Boolean, default=False)
    duration: Mapped[Optional[int]] = mapped_column(Integer)  # в минутах
    
    # Рейтинги
    rating_kp: Mapped[Optional[float]] = mapped_column(Float)
    kp_votes_count: Mapped[Optional[int]] = mapped_column(Integer)
    rating_imdb: Mapped[Optional[float]] = mapped_column(Float)
    imdb_votes_count: Mapped[Optional[int]] = mapped_column(Integer)
    user_rating: Mapped[Optional[float]] = mapped_column(Float)
    user_rating_count: Mapped[int] = mapped_column(Integer, default=0)
    
    # Бюджет и сборы
    budget: Mapped[Optional[int]] = mapped_column(Integer)
    usa_box_office: Mapped[Optional[int]] = mapped_column(Integer)
    rus_box_office: Mapped[Optional[int]] = mapped_column(Integer)
    
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
    __tablename__ = "genres"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary="film_genre", back_populates="genres"
    )


class Country(Base, IntIdPkMixin):
    """Модель страны"""
    __tablename__ = "countries"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary="film_country", back_populates="countries"
    )


class Stuff(Base, IntIdPkMixin):
    """Модель участника (актер, режиссер и т.д.)"""
    __tablename__ = "stuff"
    
    kinopoisk_id: Mapped[Optional[str]] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    original_name: Mapped[Optional[str]] = mapped_column(String(200), index=True)
    image: Mapped[Optional[str]] = mapped_column(String(500))
    career: Mapped[Optional[str]] = mapped_column(String(500))
    genres: Mapped[Optional[str]] = mapped_column(String(500))
    height: Mapped[Optional[int]] = mapped_column(Integer)
    birthday_day_month: Mapped[Optional[str]] = mapped_column(String(10))
    birthday_year: Mapped[Optional[int]] = mapped_column(Integer)
    zodiac: Mapped[Optional[str]] = mapped_column(String(50))
    age: Mapped[Optional[int]] = mapped_column(Integer)
    birthplace: Mapped[Optional[str]] = mapped_column(String(200))
    spouse: Mapped[Optional[str]] = mapped_column(String(200))
    children: Mapped[Optional[int]] = mapped_column(Integer)
    total_films: Mapped[Optional[int]] = mapped_column(Integer)
    career_start_year: Mapped[Optional[int]] = mapped_column(Integer)
    career_end_year: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary="film_stuff", back_populates="stuff"
    )


class FilmStill(Base, IntIdPkMixin):
    """Модель кадров из фильма"""
    __tablename__ = "film_stills"
    
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("films.id", ondelete="CASCADE"))
    picture_id: Mapped[str] = mapped_column(String(100), nullable=False)
    original_url: Mapped[str] = mapped_column(String(500), nullable=False)
    source: Mapped[str] = mapped_column(String(50), nullable=False)  # stills, wall
    
    # Связи
    film: Mapped["Film"] = relationship("Film", back_populates="stills")


class FilmWatchProvider(Base, IntIdPkMixin):
    """Модель провайдеров для просмотра фильма"""
    __tablename__ = "film_watch_providers"
    
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("films.id", ondelete="CASCADE"))
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    url: Mapped[str] = mapped_column(String(500), nullable=False)
    logo: Mapped[Optional[str]] = mapped_column(String(500))
    
    # Связи
    film: Mapped["Film"] = relationship("Film", back_populates="watch_providers")


class SimilarFilm(Base, IntIdPkMixin):
    """Модель похожих фильмов"""
    __tablename__ = "similar_films"
    
    film_id: Mapped[int] = mapped_column(Integer, ForeignKey("films.id", ondelete="CASCADE"))
    similar_film_id: Mapped[str] = mapped_column(String(50), nullable=False)  # kinopoisk_id
    similar_film_title: Mapped[str] = mapped_column(String(500), nullable=False)
    similar_film_year: Mapped[Optional[int]] = mapped_column(Integer)
    similar_film_genres: Mapped[Optional[str]] = mapped_column(String(500))
    similar_film_poster: Mapped[Optional[str]] = mapped_column(String(500))
    similar_film_rating: Mapped[Optional[float]] = mapped_column(Float)
    
    # Связи
    film: Mapped["Film"] = relationship("Film", back_populates="similar_films")
