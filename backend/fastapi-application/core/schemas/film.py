from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

from .genre import GenreRead
from .country import CountryRead


class FilmBase(BaseModel):
    kinopoisk_id: str = Field(..., max_length=20, description="ID в Кинопоиске")
    title: Optional[str] = Field(None, max_length=500, description="Название фильма")
    original_title: Optional[str] = Field(None, max_length=500, description="Оригинальное название")
    description: Optional[str] = Field(None, description="Краткое описание")
    full_description: Optional[str] = Field(None, description="Полное описание")
    poster: Optional[str] = Field(None, max_length=1000, description="URL постера")
    year: Optional[int] = Field(None, description="Год выпуска")
    tagline: Optional[str] = Field(None, description="Слоган")
    ru_premiere: Optional[str] = Field(None, max_length=100, description="Дата российской премьеры")
    world_premiere: Optional[str] = Field(None, max_length=100, description="Дата мировой премьеры")
    content_rating: Optional[str] = Field(None, max_length=20, description="Возрастной рейтинг")
    is_family_friendly: bool = Field(False, description="Семейный фильм")
    duration: Optional[str] = Field(None, max_length=50, description="Продолжительность")
    rating_kp: Optional[float] = Field(None, description="Рейтинг Кинопоиска")
    kp_votes_count: Optional[str] = Field(None, max_length=50, description="Количество голосов КП")
    rating_imdb: Optional[float] = Field(None, description="Рейтинг IMDB")
    imdb_votes_count: Optional[str] = Field(None, max_length=50, description="Количество голосов IMDB")
    user_rating: Optional[float] = Field(None, description="Пользовательский рейтинг")
    user_rating_count: int = Field(0, description="Количество пользовательских оценок")
    budget: Optional[str] = Field(None, max_length=100, description="Бюджет")
    usa_box_office: Optional[str] = Field(None, max_length=100, description="Сборы в США")
    rus_box_office: Optional[str] = Field(None, max_length=100, description="Сборы в России")


class FilmRead(FilmBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class FilmReadWithDetails(FilmRead):
    """Фильм с подробной информацией"""
    genres: List[GenreRead] = []
    countries: List[CountryRead] = []


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
    title: Optional[str] = Field(None, max_length=500, description="Название фильма")
    original_title: Optional[str] = Field(None, max_length=500, description="Оригинальное название")
    description: Optional[str] = Field(None, description="Краткое описание")
    full_description: Optional[str] = Field(None, description="Полное описание")
    poster: Optional[str] = Field(None, max_length=1000, description="URL постера")
    year: Optional[int] = Field(None, description="Год выпуска")
    tagline: Optional[str] = Field(None, description="Слоган")
    ru_premiere: Optional[str] = Field(None, max_length=100, description="Дата российской премьеры")
    world_premiere: Optional[str] = Field(None, max_length=100, description="Дата мировой премьеры")
    content_rating: Optional[str] = Field(None, max_length=20, description="Возрастной рейтинг")
    is_family_friendly: Optional[bool] = Field(None, description="Семейный фильм")
    duration: Optional[str] = Field(None, max_length=50, description="Продолжительность")
    rating_kp: Optional[float] = Field(None, description="Рейтинг Кинопоиска")
    kp_votes_count: Optional[str] = Field(None, max_length=50, description="Количество голосов КП")
    rating_imdb: Optional[float] = Field(None, description="Рейтинг IMDB")
    imdb_votes_count: Optional[str] = Field(None, max_length=50, description="Количество голосов IMDB")
    user_rating: Optional[float] = Field(None, description="Пользовательский рейтинг")
    user_rating_count: Optional[int] = Field(None, description="Количество пользовательских оценок")
    budget: Optional[str] = Field(None, max_length=100, description="Бюджет")
    usa_box_office: Optional[str] = Field(None, max_length=100, description="Сборы в США")
    rus_box_office: Optional[str] = Field(None, max_length=100, description="Сборы в России")
