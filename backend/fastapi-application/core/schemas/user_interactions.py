from datetime import datetime
from typing import Optional, List, Union
from pydantic import BaseModel, Field, ConfigDict

from .film import FilmRead, SeriesRead


class BookmarkBase(BaseModel):
    content_id: int = Field(..., description="ID контента")
    content_type: str = Field(..., description="Тип контента (film/series)")


class BookmarkCreate(BookmarkBase):
    pass


class BookmarkRead(BookmarkBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    created_at: datetime
    film: Optional[FilmRead] = None
    series: Optional[SeriesRead] = None


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
    content_id: int = Field(..., description="ID контента")
    content_type: str = Field(..., description="Тип контента (film/series)")


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Новое содержание комментария")


class CommentRead(CommentBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    content_id: int
    content_type: str
    is_edited: bool
    is_deleted: bool
    created_at: datetime
    edited_at: Optional[datetime] = None


class UserContentRatingBase(BaseModel):
    rating: float = Field(..., ge=1.0, le=10.0, description="Рейтинг от 1.0 до 10.0")


class UserContentRatingCreate(UserContentRatingBase):
    content_id: int = Field(..., description="ID контента")
    content_type: str = Field(..., description="Тип контента (film/series)")


class UserContentRatingUpdate(UserContentRatingBase):
    pass


class UserContentRatingRead(UserContentRatingBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    user_id: int
    content_id: int
    content_type: str
    created_at: datetime
    updated_at: datetime
    film: Optional[FilmRead] = None
    series: Optional[SeriesRead] = None


class ContentAverageRatingRead(BaseModel):
    """Средний рейтинг контента"""
    average_rating: Optional[float] = None
    total_ratings: int
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None


class UserRatingsResponse(BaseModel):
    """Ответ для рейтингов пользователя"""
    items: List[UserContentRatingRead]
    page: int
    page_size: int
    total_count: int


