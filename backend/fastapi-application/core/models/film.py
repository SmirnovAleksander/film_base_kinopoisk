from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Boolean, ForeignKey, ARRAY, UniqueConstraint, and_
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from sqlalchemy import DECIMAL

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .associations import content_genre, content_country, content_stuff

if TYPE_CHECKING:
    from .user_interactions import Bookmark, Comment, UserContentRating


class Film(Base, IntIdPkMixin):
    """Модель фильма"""
    __tablename__ = "film"
    
    kinopoisk_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    title_ru: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    title_en: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    description_short: Mapped[Optional[str]] = mapped_column(Text)
    description_full: Mapped[Optional[str]] = mapped_column(Text)
    poster_url: Mapped[Optional[str]] = mapped_column(String(1000))
    release_year: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    tagline: Mapped[Optional[str]] = mapped_column(Text)
    premiere_ru: Mapped[Optional[str]] = mapped_column(String(100))
    premiere_world: Mapped[Optional[str]] = mapped_column(String(100))
    content_type: Mapped[str] = mapped_column(String(50), default="film")
    is_family: Mapped[bool] = mapped_column(Boolean, default=False)
    duration: Mapped[Optional[str]] = mapped_column(String(50))
    
    # Рейтинги
    rating_kp: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1), index=True)
    votes_kp: Mapped[Optional[int]] = mapped_column(Integer)
    rating_imdb: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1), index=True)
    votes_imdb: Mapped[Optional[int]] = mapped_column(Integer)
    rating_user: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1))
    votes_user: Mapped[int] = mapped_column(Integer, default=0)
    
    # Бюджет и сборы
    budget: Mapped[Optional[str]] = mapped_column(String(100))
    box_office_usa: Mapped[Optional[str]] = mapped_column(String(100))
    box_office_rus: Mapped[Optional[str]] = mapped_column(String(100))
    
    # Связи
    genres: Mapped[List["Genre"]] = relationship(
        "Genre", 
        secondary=content_genre, 
        primaryjoin="and_(Film.id==foreign(content_genre.c.content_id), content_genre.c.content_type=='film')",
        secondaryjoin="Genre.id==foreign(content_genre.c.genre_id)",
        back_populates="films"
    )
    countries: Mapped[List["Country"]] = relationship(
        "Country", 
        secondary=content_country,
        primaryjoin="and_(Film.id==foreign(content_country.c.content_id), content_country.c.content_type=='film')",
        secondaryjoin="Country.id==foreign(content_country.c.country_id)",
        back_populates="films"
    )
    stuff: Mapped[List["Stuff"]] = relationship(
        "Stuff", 
        secondary=content_stuff,
        primaryjoin="and_(Film.id==foreign(content_stuff.c.content_id), content_stuff.c.content_type=='film')",
        secondaryjoin="Stuff.id==foreign(content_stuff.c.stuff_id)",
        back_populates="films"
    )
    bookmarks: Mapped[List["Bookmark"]] = relationship(
        "Bookmark", 
        primaryjoin="and_(Film.id==foreign(Bookmark.content_id), Bookmark.content_type=='film')",
        back_populates="film", 
        cascade="all, delete-orphan",
        overlaps="bookmarks"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", 
        primaryjoin="and_(Film.id==foreign(Comment.content_id), Comment.content_type=='film')",
        back_populates="film", 
        cascade="all, delete-orphan",
        overlaps="comments"
    )
    ratings: Mapped[List["UserContentRating"]] = relationship(
        "UserContentRating", 
        primaryjoin="and_(Film.id==foreign(UserContentRating.content_id), UserContentRating.content_type=='film')",
        back_populates="film", 
        cascade="all, delete-orphan",
        overlaps="ratings"
    )
    images: Mapped[List["ContentImage"]] = relationship(
        "ContentImage", 
        primaryjoin="and_(Film.id==foreign(ContentImage.content_id), ContentImage.content_type=='film')",
        back_populates="film", 
        cascade="all, delete-orphan",
        overlaps="film"
    )
    watch_providers: Mapped[List["ContentWatchProvider"]] = relationship(
        "ContentWatchProvider", 
        primaryjoin="and_(Film.id==foreign(ContentWatchProvider.content_id), ContentWatchProvider.content_type=='film')",
        back_populates="film", 
        cascade="all, delete-orphan"
    )
    similar_content: Mapped[List["SimilarContent"]] = relationship(
        "SimilarContent", 
        primaryjoin="and_(Film.id==foreign(SimilarContent.content_id), SimilarContent.content_type=='film')",
        back_populates="film", 
        cascade="all, delete-orphan"
    )


class Series(Base, IntIdPkMixin):
    """Модель сериала"""
    __tablename__ = "series"
    
    kinopoisk_id: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    title_ru: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    title_en: Mapped[Optional[str]] = mapped_column(String(500), index=True)
    description_short: Mapped[Optional[str]] = mapped_column(Text)
    description_full: Mapped[Optional[str]] = mapped_column(Text)
    poster_url: Mapped[Optional[str]] = mapped_column(String(1000))
    release_year: Mapped[Optional[int]] = mapped_column(Integer, index=True)
    tagline: Mapped[Optional[str]] = mapped_column(Text)
    premiere_ru: Mapped[Optional[str]] = mapped_column(String(100))
    premiere_world: Mapped[Optional[str]] = mapped_column(String(100))
    content_type: Mapped[str] = mapped_column(String(50), default="series")
    is_family: Mapped[bool] = mapped_column(Boolean, default=False)
    
    # Рейтинги
    rating_kp: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1), index=True)
    votes_kp: Mapped[Optional[int]] = mapped_column(Integer)
    rating_imdb: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1), index=True)
    votes_imdb: Mapped[Optional[int]] = mapped_column(Integer)
    rating_user: Mapped[Optional[float]] = mapped_column(DECIMAL(3, 1))
    votes_user: Mapped[int] = mapped_column(Integer, default=0)
    
    platform: Mapped[Optional[str]] = mapped_column(String(200))
    episodes_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Связи
    genres: Mapped[List["Genre"]] = relationship(
        "Genre", 
        secondary=content_genre,
        primaryjoin="and_(Series.id==foreign(content_genre.c.content_id), content_genre.c.content_type=='series')",
        secondaryjoin="Genre.id==foreign(content_genre.c.genre_id)",
        back_populates="series"
    )
    countries: Mapped[List["Country"]] = relationship(
        "Country", 
        secondary=content_country,
        primaryjoin="and_(Series.id==foreign(content_country.c.content_id), content_country.c.content_type=='series')",
        secondaryjoin="Country.id==foreign(content_country.c.country_id)",
        back_populates="series"
    )
    stuff: Mapped[List["Stuff"]] = relationship(
        "Stuff", 
        secondary=content_stuff,
        primaryjoin="and_(Series.id==foreign(content_stuff.c.content_id), content_stuff.c.content_type=='series')",
        secondaryjoin="Stuff.id==foreign(content_stuff.c.stuff_id)",
        back_populates="series"
    )
    bookmarks: Mapped[List["Bookmark"]] = relationship(
        "Bookmark", 
        primaryjoin="and_(Series.id==foreign(Bookmark.content_id), Bookmark.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan",
        overlaps="bookmarks"
    )
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", 
        primaryjoin="and_(Series.id==foreign(Comment.content_id), Comment.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan",
        overlaps="comments"
    )
    ratings: Mapped[List["UserContentRating"]] = relationship(
        "UserContentRating", 
        primaryjoin="and_(Series.id==foreign(UserContentRating.content_id), UserContentRating.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan",
        overlaps="ratings"
    )
    images: Mapped[List["ContentImage"]] = relationship(
        "ContentImage", 
        primaryjoin="and_(Series.id==foreign(ContentImage.content_id), ContentImage.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan",
        overlaps="series"
    )
    watch_providers: Mapped[List["ContentWatchProvider"]] = relationship(
        "ContentWatchProvider", 
        primaryjoin="and_(Series.id==foreign(ContentWatchProvider.content_id), ContentWatchProvider.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan"
    )
    similar_content: Mapped[List["SimilarContent"]] = relationship(
        "SimilarContent", 
        primaryjoin="and_(Series.id==foreign(SimilarContent.content_id), SimilarContent.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan"
    )


class Genre(Base, IntIdPkMixin):
    """Модель жанра"""
    __tablename__ = "genre"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary=content_genre,
        primaryjoin="and_(Genre.id==foreign(content_genre.c.genre_id), content_genre.c.content_type=='film')",
        secondaryjoin="Film.id==foreign(content_genre.c.content_id)",
        back_populates="genres"
    )
    series: Mapped[List["Series"]] = relationship(
        "Series", secondary=content_genre,
        primaryjoin="and_(Genre.id==foreign(content_genre.c.genre_id), content_genre.c.content_type=='series')",
        secondaryjoin="Series.id==foreign(content_genre.c.content_id)",
        back_populates="genres"
    )


class Country(Base, IntIdPkMixin):
    """Модель страны"""
    __tablename__ = "country"
    
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True, index=True)
    
    # Связи
    films: Mapped[List["Film"]] = relationship(
        "Film", secondary=content_country,
        primaryjoin="and_(Country.id==foreign(content_country.c.country_id), content_country.c.content_type=='film')",
        secondaryjoin="Film.id==foreign(content_country.c.content_id)",
        back_populates="countries"
    )
    series: Mapped[List["Series"]] = relationship(
        "Series", secondary=content_country,
        primaryjoin="and_(Country.id==foreign(content_country.c.country_id), content_country.c.content_type=='series')",
        secondaryjoin="Series.id==foreign(content_country.c.content_id)",
        back_populates="countries"
    )


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
        back_populates="stuff"
    )
    series: Mapped[List["Series"]] = relationship(
        "Series", secondary=content_stuff,
        primaryjoin="and_(Stuff.id==foreign(content_stuff.c.stuff_id), content_stuff.c.content_type=='series')",
        secondaryjoin="Series.id==foreign(content_stuff.c.content_id)",
        back_populates="stuff"
    )
    images: Mapped[List["StuffImage"]] = relationship("StuffImage", back_populates="stuff", cascade="all, delete-orphan")
    filmography: Mapped[List["StuffFilmography"]] = relationship("StuffFilmography", back_populates="stuff", cascade="all, delete-orphan")


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
    
    # Связи
    film: Mapped["Film"] = relationship(
        "Film", 
        primaryjoin="and_(Film.id==foreign(ContentImage.content_id), ContentImage.content_type=='film')",
        back_populates="images",
        overlaps="film"
    )
    series: Mapped["Series"] = relationship(
        "Series", 
        primaryjoin="and_(Series.id==foreign(ContentImage.content_id), ContentImage.content_type=='series')",
        back_populates="images",
        overlaps="series"
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
        back_populates="watch_providers"
    )
    series: Mapped["Series"] = relationship(
        "Series", 
        primaryjoin="and_(Series.id==foreign(ContentWatchProvider.content_id), ContentWatchProvider.content_type=='series')",
        back_populates="watch_providers"
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
        back_populates="similar_content"
    )
    series: Mapped["Series"] = relationship(
        "Series", 
        primaryjoin="and_(Series.id==foreign(SimilarContent.content_id), SimilarContent.content_type=='series')",
        back_populates="similar_content"
    )


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
