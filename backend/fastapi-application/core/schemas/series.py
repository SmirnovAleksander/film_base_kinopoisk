from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from .genres import GenreRead
from .countries import CountryRead
from .stuff import StuffRead
from .content_details import (
    ContentImageRead,
    ContentWatchProviderRead,
    SimilarContentRead,
)


class SeriesBase(BaseModel):
    kinopoisk_id: str = Field(..., max_length=20, description="ID в Кинопоиске")
    title_ru: Optional[str] = Field(None, max_length=500, description="Название сериала")
    title_en: Optional[str] = Field(None, max_length=500, description="Оригинальное название")
    description_short: Optional[str] = Field(None, description="Краткое описание")
    description_full: Optional[str] = Field(None, description="Полное описание")
    poster_url: Optional[str] = Field(None, max_length=1000, description="URL постера")
    release_year: Optional[int] = Field(None, description="Год выпуска")
    tagline: Optional[str] = Field(None, description="Слоган")
    premiere_ru: Optional[str] = Field(None, max_length=100, description="Дата российской премьеры")
    premiere_world: Optional[str] = Field(None, max_length=100, description="Дата мировой премьеры")
    content_type: str = Field("series", max_length=50, description="Тип контента")
    is_family: bool = Field(False, description="Семейный сериал")
    rating_kp: Optional[float] = Field(None, description="Рейтинг Кинопоиска")
    votes_kp: Optional[int] = Field(None, description="Количество голосов КП")
    rating_imdb: Optional[float] = Field(None, description="Рейтинг IMDB")
    votes_imdb: Optional[int] = Field(None, description="Количество голосов IMDB")
    rating_user: Optional[float] = Field(None, description="Пользовательский рейтинг")
    votes_user: int = Field(0, description="Количество пользовательских оценок")
    platform: Optional[str] = Field(None, max_length=200, description="Платформа")
    episodes_count: Optional[int] = Field(None, description="Количество эпизодов")


class SeriesRead(SeriesBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class SeriesReadWithDetails(SeriesRead):
    """Сериал с подробной информацией"""
    genres: List[GenreRead] = []
    countries: List[CountryRead] = []
    stuff: List[StuffRead] = []
    images: List[ContentImageRead] = []
    watch_providers: List[ContentWatchProviderRead] = []
    similar_content: List[SimilarContentRead] = []


class SeriesUpdate(BaseModel):
    """Схема для обновления сериала"""
    title_ru: Optional[str] = Field(None, max_length=500)
    title_en: Optional[str] = Field(None, max_length=500)
    description_short: Optional[str] = None
    description_full: Optional[str] = None
    poster_url: Optional[str] = Field(None, max_length=1000)
    release_year: Optional[int] = None
    tagline: Optional[str] = None
    premiere_ru: Optional[str] = Field(None, max_length=100)
    premiere_world: Optional[str] = Field(None, max_length=100)
    is_family: Optional[bool] = None
    rating_kp: Optional[float] = None
    votes_kp: Optional[int] = None
    rating_imdb: Optional[float] = None
    votes_imdb: Optional[int] = None
    rating_user: Optional[float] = None
    votes_user: Optional[int] = None
    platform: Optional[str] = Field(None, max_length=200)
    episodes_count: Optional[int] = None
