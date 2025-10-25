from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class MediaBase(BaseModel):
    url: str = Field(..., max_length=500, description="URL медиа контента")
    title: str = Field(..., max_length=1000, description="Заголовок")
    image: Optional[str] = Field(None, max_length=1000, description="URL изображения")
    category: Optional[str] = Field(None, max_length=100, description="Категория")
    date: Optional[str] = Field(None, max_length=100, description="Дата публикации")
    comments_count: int = Field(0, description="Количество комментариев")
    card_type: Optional[str] = Field(None, max_length=20, description="Тип карточки")
    type: str = Field("news", max_length=20, description="Тип контента")


class MediaRead(MediaBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    parsed_at: datetime


class MediaResponse(BaseModel):
    """Ответ для списка медиа"""
    media: List[MediaRead]
    pagination: dict


class MediaCategoriesResponse(BaseModel):
    """Ответ для категорий медиа"""
    categories: List[str]


class MediaTypesResponse(BaseModel):
    """Ответ для типов медиа"""
    types: List[str]


class MediaStatsResponse(BaseModel):
    """Статистика медиа"""
    total_media: int
    categories: dict
    card_types: dict
    content_types: dict
