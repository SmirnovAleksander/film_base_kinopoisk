from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class FilmGenreRead(BaseModel):
    """Схема для чтения связи фильм-жанр"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    film_id: int
    genre_id: int


class FilmGenreCreate(BaseModel):
    """Схема для создания связи фильм-жанр"""
    film_id: int = Field(..., description="ID фильма")
    genre_id: int = Field(..., description="ID жанра")


class FilmCountryRead(BaseModel):
    """Схема для чтения связи фильм-страна"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    film_id: int
    country_id: int


class FilmCountryCreate(BaseModel):
    """Схема для создания связи фильм-страна"""
    film_id: int = Field(..., description="ID фильма")
    country_id: int = Field(..., description="ID страны")


class FilmStuffRead(BaseModel):
    """Схема для чтения связи фильм-участник"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    film_id: int
    stuff_id: int
    role: Optional[str] = Field(None, max_length=100, description="Роль участника")


class FilmStuffCreate(BaseModel):
    """Схема для создания связи фильм-участник"""
    film_id: int = Field(..., description="ID фильма")
    stuff_id: int = Field(..., description="ID участника")
    role: Optional[str] = Field(None, max_length=100, description="Роль участника (actor, director, writer и т.д.)")


class FilmStuffUpdate(BaseModel):
    """Схема для обновления связи фильм-участник"""
    role: Optional[str] = Field(None, max_length=100, description="Роль участника")
