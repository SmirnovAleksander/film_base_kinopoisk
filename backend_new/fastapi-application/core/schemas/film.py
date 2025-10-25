from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class GenreBase(BaseModel):
    name: str = Field(..., max_length=100, description="Название жанра")


class GenreRead(GenreBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    

class CountryBase(BaseModel):
    name: str = Field(..., max_length=100, description="Название страны")


class CountryRead(CountryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class StuffBase(BaseModel):
    kinopoisk_id: Optional[str] = Field(None, max_length=50, description="ID в Кинопоиске")
    name: str = Field(..., max_length=200, description="Имя участника")
    original_name: Optional[str] = Field(None, max_length=200, description="Оригинальное имя")
    image: Optional[str] = Field(None, max_length=500, description="URL изображения")
    career: Optional[str] = Field(None, max_length=500, description="Карьера")
    genres: Optional[str] = Field(None, max_length=500, description="Жанры")
    height: Optional[int] = Field(None, description="Рост в см")
    birthday_day_month: Optional[str] = Field(None, max_length=10, description="День и месяц рождения")
    birthday_year: Optional[int] = Field(None, description="Год рождения")
    zodiac: Optional[str] = Field(None, max_length=50, description="Знак зодиака")
    age: Optional[int] = Field(None, description="Возраст")
    birthplace: Optional[str] = Field(None, max_length=200, description="Место рождения")
    spouse: Optional[str] = Field(None, max_length=200, description="Супруг(а)")
    children: Optional[int] = Field(None, description="Количество детей")
    total_films: Optional[int] = Field(None, description="Общее количество фильмов")
    career_start_year: Optional[int] = Field(None, description="Год начала карьеры")
    career_end_year: Optional[int] = Field(None, description="Год окончания карьеры")


class StuffRead(StuffBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class FilmStillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    picture_id: str
    original_url: str
    source: str


class FilmWatchProviderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    url: str
    logo: Optional[str] = None


class SimilarFilmRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    kinopoisk_id: str
    title: str
    year: Optional[int] = None
    genres: Optional[str] = None
    poster: Optional[str] = None
    rating: Optional[float] = None


class FilmBase(BaseModel):
    kinopoisk_id: Optional[str] = Field(None, max_length=50, description="ID в Кинопоиске")
    title: str = Field(..., max_length=500, description="Название фильма")
    original_title: Optional[str] = Field(None, max_length=500, description="Оригинальное название")
    description: Optional[str] = Field(None, description="Краткое описание")
    full_description: Optional[str] = Field(None, description="Полное описание")
    poster: Optional[str] = Field(None, max_length=500, description="URL постера")
    year: Optional[int] = Field(None, description="Год выпуска")
    tagline: Optional[str] = Field(None, max_length=500, description="Слоган")
    ru_premiere: Optional[datetime] = Field(None, description="Дата российской премьеры")
    world_premiere: Optional[datetime] = Field(None, description="Дата мировой премьеры")
    content_rating: Optional[str] = Field(None, max_length=10, description="Возрастной рейтинг")
    is_family_friendly: bool = Field(False, description="Семейный фильм")
    duration: Optional[int] = Field(None, description="Продолжительность в минутах")
    rating_kp: Optional[float] = Field(None, description="Рейтинг Кинопоиска")
    kp_votes_count: Optional[int] = Field(None, description="Количество голосов КП")
    rating_imdb: Optional[float] = Field(None, description="Рейтинг IMDB")
    imdb_votes_count: Optional[int] = Field(None, description="Количество голосов IMDB")
    user_rating: Optional[float] = Field(None, description="Пользовательский рейтинг")
    user_rating_count: int = Field(0, description="Количество пользовательских оценок")
    budget: Optional[int] = Field(None, description="Бюджет")
    usa_box_office: Optional[int] = Field(None, description="Сборы в США")
    rus_box_office: Optional[int] = Field(None, description="Сборы в России")


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
