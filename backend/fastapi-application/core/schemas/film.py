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


class FilmBase(BaseModel):
    kinopoisk_id: str = Field(..., max_length=20, description="ID в Кинопоиске")
    title_ru: Optional[str] = Field(None, max_length=500, description="Название фильма")
    title_en: Optional[str] = Field(None, max_length=500, description="Оригинальное название")
    description_short: Optional[str] = Field(None, description="Краткое описание")
    description_full: Optional[str] = Field(None, description="Полное описание")
    poster_url: Optional[str] = Field(None, max_length=1000, description="URL постера")
    release_year: Optional[int] = Field(None, description="Год выпуска")
    tagline: Optional[str] = Field(None, description="Слоган")
    premiere_ru: Optional[str] = Field(None, max_length=100, description="Дата российской премьеры")
    premiere_world: Optional[str] = Field(None, max_length=100, description="Дата мировой премьеры")
    content_type: str = Field("film", max_length=50, description="Тип контента")
    is_family: bool = Field(False, description="Семейный фильм")
    duration: Optional[str] = Field(None, max_length=50, description="Продолжительность")
    rating_kp: Optional[float] = Field(None, description="Рейтинг Кинопоиска")
    votes_kp: Optional[int] = Field(None, description="Количество голосов КП")
    rating_imdb: Optional[float] = Field(None, description="Рейтинг IMDB")
    votes_imdb: Optional[int] = Field(None, description="Количество голосов IMDB")
    budget: Optional[str] = Field(None, max_length=100, description="Бюджет")
    box_office_usa: Optional[str] = Field(None, max_length=100, description="Сборы в США")
    box_office_rus: Optional[str] = Field(None, max_length=100, description="Сборы в России")


class FilmRead(FilmBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    rating_user: Optional[float] = Field(None, description="Пользовательский рейтинг")
    votes_user: int = Field(0, description="Количество пользовательских оценок")


class FilmReadWithDetails(FilmRead):
    """Фильм с подробной информацией"""
    genres: List[GenreRead] = []
    countries: List[CountryRead] = []
    stuff: List[StuffRead] = []
    images: List[ContentImageRead] = []
    watch_providers: List[ContentWatchProviderRead] = []
    similar_content: List[SimilarContentRead] = []


class FilmSearchResponse(BaseModel):
    """Ответ для поиска фильмов"""
    items: List[FilmRead]
    page: int
    page_size: int
    total_count: int


class FilmFilterParams(BaseModel):
    """Параметры фильтрации фильмов"""
    genre_id: Optional[int] = None
    country_id: Optional[int] = None
    start_year: Optional[int] = None
    end_year: Optional[int] = None
    title: Optional[str] = None
    lang: str = Field("ru", description="Язык поиска: ru или en")
    source: str = Field("kp", description="Источник рейтинга: kp или imdb")
    min_rating: Optional[float] = None
    max_rating: Optional[float] = None


class FilmRecommendationRead(FilmRead):
    """Рекомендация фильма"""
    relevance_score: float = Field(..., description="Оценка релевантности")
    genre_matches: int = Field(..., description="Совпадения по жанрам")
    stuff_matches: int = Field(..., description="Совпадения по участникам")


class FilmRecommendationsResponse(BaseModel):
    """Ответ для рекомендаций фильмов"""
    items: List[FilmRecommendationRead]
    total_count: int


class FilmCreate(FilmBase):
    """Схема для создания фильма"""
    pass


class FilmUpdate(BaseModel):
    """Схема для обновления фильма"""
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
    duration: Optional[str] = Field(None, max_length=50)
    rating_kp: Optional[float] = None
    votes_kp: Optional[int] = None
    rating_imdb: Optional[float] = None
    votes_imdb: Optional[int] = None
    budget: Optional[str] = Field(None, max_length=100)
    box_office_usa: Optional[str] = Field(None, max_length=100)
    box_office_rus: Optional[str] = Field(None, max_length=100)
