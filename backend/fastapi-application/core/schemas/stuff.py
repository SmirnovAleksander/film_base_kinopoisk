from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


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


class StuffSearchResponse(BaseModel):
    """Ответ для поиска участников"""
    items: List[StuffRead]
    page: int
    page_size: int
    total_count: int


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
