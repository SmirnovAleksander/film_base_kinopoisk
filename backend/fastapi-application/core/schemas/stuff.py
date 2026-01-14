from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class StuffBase(BaseModel):
    kinopoisk_id: str = Field(..., max_length=20, description="ID в Кинопоиске")
    name: Optional[str] = Field(None, max_length=200, description="Имя участника")
    original_name: Optional[str] = Field(None, max_length=200, description="Оригинальное имя")
    career: Optional[List[str]] = Field(None, description="Карьера")
    ganres: Optional[List[str]] = Field(None, description="Жанры")
    height: Optional[str] = Field(None, max_length=50, description="Рост")
    birthday_day_month: Optional[str] = Field(None, max_length=50, description="День и месяц рождения")
    zodiac: Optional[str] = Field(None, max_length=50, description="Знак зодиака")
    age: Optional[int] = Field(None, description="Возраст")
    birthplace: Optional[List[str]] = Field(None, description="Место рождения")
    spouse: Optional[List[str]] = Field(None, description="Супруг(а)")
    children: Optional[List[str]] = Field(None, description="Дети")
    total_films: Optional[int] = Field(None, description="Общее количество фильмов")
    career_start_year: Optional[int] = Field(None, description="Год начала карьеры")
    career_end_year: Optional[int] = Field(None, description="Год окончания карьеры")
    image: Optional[str] = Field(None, max_length=1000, description="URL изображения")


class StuffRead(StuffBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class StuffCreate(StuffBase):
    """Схема для создания участника"""
    pass


class StuffUpdate(BaseModel):
    """Схема для обновления участника"""
    name: Optional[str] = Field(None, max_length=200, description="Имя участника")
    original_name: Optional[str] = Field(None, max_length=200, description="Оригинальное имя")
    career: Optional[List[str]] = Field(None, description="Карьера")
    ganres: Optional[List[str]] = Field(None, description="Жанры")
    height: Optional[str] = Field(None, max_length=50, description="Рост")
    birthday_day_month: Optional[str] = Field(None, max_length=50, description="День и месяц рождения")
    zodiac: Optional[str] = Field(None, max_length=50, description="Знак зодиака")
    age: Optional[int] = Field(None, description="Возраст")
    birthplace: Optional[List[str]] = Field(None, description="Место рождения")
    spouse: Optional[List[str]] = Field(None, description="Супруг(а)")
    children: Optional[List[str]] = Field(None, description="Дети")
    total_films: Optional[int] = Field(None, description="Общее количество фильмов")
    career_start_year: Optional[int] = Field(None, description="Год начала карьеры")
    career_end_year: Optional[int] = Field(None, description="Год окончания карьеры")
    image: Optional[str] = Field(None, max_length=1000, description="URL изображения")


class StuffListResponse(BaseModel):
    """Ответ для списка участников"""
    items: List[StuffRead]
    page: int
    page_size: int
    total_count: int
