from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from .film import FilmRead


class BookmarkBase(BaseModel):
    film_id: int = Field(..., description="ID фильма")


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkRead(BookmarkBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime
    film: Optional[FilmRead] = None


class BookmarkResponse(BaseModel):
    """Ответ для операций с закладками"""
    items: List[BookmarkRead]
    page: int
    page_size: int
    total_count: int


class BookmarkStatusResponse(BaseModel):
    """Статус закладки"""
    is_bookmarked: bool
    bookmark_id: Optional[int] = None
    bookmarked_at: Optional[datetime] = None


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Содержание комментария")


class CommentCreate(CommentBase):
    film_id: int = Field(..., description="ID фильма")


class CommentUpdate(CommentBase):
    """Схема для обновления комментария"""
    pass


class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    film_id: int
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    edited_at: Optional[datetime] = None


class UserFilmRatingBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=10.0, description="Рейтинг от 1.0 до 10.0")


class UserFilmRatingCreate(UserFilmRatingBase):
    film_id: int = Field(..., description="ID фильма")


class UserFilmRatingUpdate(UserFilmRatingBase):
    pass


class UserFilmRatingRead(UserFilmRatingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    film_id: int
    created_at: datetime
    updated_at: datetime
    film: Optional[FilmRead] = None


class FilmAverageRatingRead(BaseModel):
    """Средний рейтинг фильма"""
    average_rating: Optional[float] = None
    total_ratings: int
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None


class UserRatingsResponse(BaseModel):
    """Ответ для рейтингов пользователя"""
    items: List[UserFilmRatingRead]
    page: int
    page_size: int
    total_count: int
