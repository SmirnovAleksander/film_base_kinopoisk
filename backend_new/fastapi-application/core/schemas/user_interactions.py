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


class BookmarkStatusResponse(BaseModel):
    """Статус закладки"""
    is_bookmarked: bool
    bookmark_id: Optional[int] = None
    bookmarked_at: Optional[datetime] = None


class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Содержание комментария")


class CommentCreate(CommentBase):
    film_id: int = Field(..., description="ID фильма")


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Новое содержание комментария")


class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    film_id: int
    is_edited: bool
    is_deleted: bool
    status: str
    created_at: datetime
    edited_at: Optional[datetime] = None
    moderated_at: Optional[datetime] = None


class CommentModerationRead(CommentRead):
    """Комментарий для модерации с дополнительной информацией"""
    film_title: Optional[str] = None
    user_email: Optional[str] = None
    username: Optional[str] = None


class CommentModerationResponse(BaseModel):
    """Ответ для модерации комментариев"""
    items: List[CommentModerationRead]
    page: int
    page_size: int
    total_count: int
    total_pages: int


class CommentModerationStats(BaseModel):
    """Статистика модерации комментариев"""
    total_comments: int
    status_distribution: dict
    comments_7d: int
    pending_comments: int


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


class UserFilmHistoryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    visited_at: datetime
    film: FilmRead


class UserFilmHistoryResponse(BaseModel):
    """Ответ для истории просмотров"""
    history: List[UserFilmHistoryRead]
    total: int


class UserFilmHistoryStats(BaseModel):
    """Статистика истории просмотров"""
    total_visits: int
    visits_7d: int
    visits_30d: int
    favorite_genre: Optional[str] = None
    favorite_genre_count: int = 0
