from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class GenreBase(BaseModel):
    name: str = Field(..., max_length=100, description="Название жанра")


class GenreCreate(GenreBase):
    pass


class GenreUpdate(BaseModel):
    name: str = Field(..., max_length=100, description="Название жанра")


class GenreRead(GenreBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    

class CountryBase(BaseModel):
    name: str = Field(..., max_length=100, description="Название страны")


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: str = Field(..., max_length=100, description="Название страны")


class CountryRead(CountryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class StuffBase(BaseModel):
    kinopoisk_id: str = Field(..., max_length=20, description="ID в Кинопоиске")
    name_ru: Optional[str] = Field(None, max_length=200, description="Имя участника")
    name_en: Optional[str] = Field(None, max_length=200, description="Оригинальное имя")
    career: Optional[List[str]] = Field(None, description="Карьера")
    genres: Optional[List[str]] = Field(None, description="Жанры")
    height: Optional[str] = Field(None, max_length=50, description="Рост")
    zodiac: Optional[str] = Field(None, max_length=50, description="Знак зодиака")
    birth_date: Optional[str] = Field(None, max_length=100, description="Дата рождения")
    birth_place: Optional[List[str]] = Field(None, description="Место рождения")
    spouse: Optional[List[str]] = Field(None, description="Супруг(а)")
    children: Optional[List[str]] = Field(None, description="Дети")
    films_total: Optional[int] = Field(None, description="Общее количество фильмов")
    career_start: Optional[int] = Field(None, description="Год начала карьеры")
    photo_url: Optional[str] = Field(None, max_length=1000, description="URL изображения")


class StuffRead(StuffBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class StuffImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    stuff_id: int
    picture_id: str
    image_url: str
    image_type: str


class StuffFilmographyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    stuff_id: int
    content_id: str
    title_ru: Optional[str] = None
    title_en: Optional[str] = None
    release_year: Optional[int] = None
    genres: Optional[str] = None
    countries: Optional[str] = None
    poster_url: Optional[str] = None
    rating_kp: Optional[float] = None
    votes_kp: Optional[int] = None
    role: Optional[str] = None
    release_year_start: Optional[int] = None
    release_year_end: Optional[int] = None


class ContentImageCreate(BaseModel):
    content_id: int
    content_type: str
    picture_id: str
    image_url: str
    image_type: str


class ContentImageRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    content_id: int
    content_type: str
    picture_id: str
    image_url: str
    image_type: str


class ContentWatchProviderCreate(BaseModel):
    content_id: int
    content_type: str
    provider_name: str
    provider_url: str
    provider_logo: Optional[str] = None


class ContentWatchProviderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    content_id: int
    content_type: str
    provider_name: str
    provider_url: str
    provider_logo: Optional[str] = None


class SimilarContentCreate(BaseModel):
    content_id: int
    content_type: str
    similar_id: str
    similar_type: str
    title_ru: Optional[str] = None
    release_year: Optional[int] = None
    genres: Optional[List[str]] = None
    poster_url: Optional[str] = None
    rating_kp: Optional[float] = None


class SimilarContentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    content_id: int
    content_type: str
    similar_id: str
    similar_type: str
    title_ru: Optional[str] = None
    release_year: Optional[int] = None
    genres: Optional[List[str]] = None
    poster_url: Optional[str] = None
    rating_kp: Optional[float] = None


class ContentGenreRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content_id: int
    content_type: str
    genre_id: int


class ContentGenreCreate(BaseModel):
    content_id: int
    content_type: str
    genre_id: int


class ContentCountryRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content_id: int
    content_type: str
    country_id: int


class ContentCountryCreate(BaseModel):
    content_id: int
    content_type: str
    country_id: int


class ContentStuffRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    content_id: int
    content_type: str
    stuff_id: int
    role: Optional[str] = None


class ContentStuffCreate(BaseModel):
    content_id: int
    content_type: str
    stuff_id: int
    role: Optional[str] = None


class FilmBase(BaseModel):
    kinopoisk_id: str = Field(..., max_length=20, description="ID в Кинопоиске")
    title_ru: Optional[str] = Field(None, max_length=500, description="Название фильма")
    title_en: Optional[str] = Field(None, max_length=500, description="Оригинальное название")
    description_short: Optional[str] = Field(None, description="Краткое описание")
    description_full: Optional[Optional[str]] = Field(None, description="Полное описание")
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
    rating_user: Optional[float] = Field(None, description="Пользовательский рейтинг")
    votes_user: int = Field(0, description="Количество пользовательских оценок")
    budget: Optional[str] = Field(None, max_length=100, description="Бюджет")
    box_office_usa: Optional[str] = Field(None, max_length=100, description="Сборы в США")
    box_office_rus: Optional[str] = Field(None, max_length=100, description="Сборы в России")


class FilmRead(FilmBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int


class FilmReadWithDetails(FilmRead):
    """Фильм с подробной информацией"""
    genres: List[GenreRead] = []
    countries: List[CountryRead] = []
    stuff: List[StuffRead] = []
    images: List[ContentImageRead] = []
    watch_providers: List[ContentWatchProviderRead] = []
    similar_content: List[SimilarContentRead] = []


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


class StuffSearchResponse(BaseModel):
    """Ответ для поиска участников"""
    items: List[StuffRead]
    page: int
    page_size: int
    total_count: int


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
    rating_user: Optional[float] = None
    votes_user: Optional[int] = None


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


class StuffCreate(StuffBase):
    """Схема для создания участника"""
    pass


class StuffUpdate(BaseModel):
    """Схема для обновления участника"""
    name_ru: Optional[str] = Field(None, max_length=200)
    name_en: Optional[str] = Field(None, max_length=200)
    career: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    height: Optional[str] = Field(None, max_length=50)
    zodiac: Optional[str] = Field(None, max_length=50)
    birth_date: Optional[str] = Field(None, max_length=100)
    birth_place: Optional[List[str]] = None
    spouse: Optional[List[str]] = None
    children: Optional[List[str]] = None
    films_total: Optional[int] = None
    career_start: Optional[int] = None
    photo_url: Optional[str] = Field(None, max_length=1000)
