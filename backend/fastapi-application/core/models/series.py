from typing import Optional, List, TYPE_CHECKING
from sqlalchemy import String, Integer, Text, Boolean, DECIMAL
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign

from .base import Base
from .mixins.int_id_pk import IntIdPkMixin
from .associations import content_genre, content_country, content_stuff

if TYPE_CHECKING:
    from .genre import Genre
    from .country import Country
    from .stuff import Stuff
    from .content_details import ContentImage, ContentWatchProvider, SimilarContent
    from .user_interactions import Bookmark, Comment, UserContentRating, ContentUserRating


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
    
    platform: Mapped[Optional[str]] = mapped_column(String(200))
    episodes_count: Mapped[Optional[int]] = mapped_column(Integer)
    
    # Связи
    genres: Mapped[List["Genre"]] = relationship(
        "Genre", 
        secondary=content_genre,
        primaryjoin="and_(Series.id==foreign(content_genre.c.content_id), content_genre.c.content_type=='series')",
        secondaryjoin="Genre.id==foreign(content_genre.c.genre_id)",
        back_populates="series",
        overlaps="genres"
    )
    countries: Mapped[List["Country"]] = relationship(
        "Country", 
        secondary=content_country,
        primaryjoin="and_(Series.id==foreign(content_country.c.content_id), content_country.c.content_type=='series')",
        secondaryjoin="Country.id==foreign(content_country.c.country_id)",
        back_populates="series",
        overlaps="countries"
    )
    stuff: Mapped[List["Stuff"]] = relationship(
        "Stuff", 
        secondary=content_stuff,
        primaryjoin="and_(Series.id==foreign(content_stuff.c.content_id), content_stuff.c.content_type=='series')",
        secondaryjoin="Stuff.id==foreign(content_stuff.c.stuff_id)",
        back_populates="series",
        overlaps="stuff"
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
        overlaps="images"
    )
    watch_providers: Mapped[List["ContentWatchProvider"]] = relationship(
        "ContentWatchProvider", 
        primaryjoin="and_(Series.id==foreign(ContentWatchProvider.content_id), ContentWatchProvider.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan",
        overlaps="watch_providers"
    )
    similar_content: Mapped[List["SimilarContent"]] = relationship(
        "SimilarContent", 
        primaryjoin="and_(Series.id==foreign(SimilarContent.content_id), SimilarContent.content_type=='series')",
        back_populates="series", 
        cascade="all, delete-orphan",
        overlaps="similar_content"
    )
    user_rating: Mapped["ContentUserRating"] = relationship(
        "ContentUserRating",
        primaryjoin="and_(Series.id==foreign(ContentUserRating.content_id), ContentUserRating.content_type=='series')",
        back_populates="series",
        uselist=False,
        cascade="all, delete-orphan",
        overlaps="user_rating"
    )

    @property
    def rating_user(self) -> Optional[float]:
        return self.user_rating.rating_user if self.user_rating else None

    @property
    def votes_user(self) -> int:
        return self.user_rating.votes_user if self.user_rating else 0
