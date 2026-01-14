from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class FilmStillRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    picture_id: str
    original_url: str
    source: str
    film_id: int


class FilmStillCreate(BaseModel):
    film_id: int = Field(..., description="ID фильма")
    picture_id: str = Field(..., max_length=50, description="ID изображения")
    original_url: str = Field(..., description="URL оригинального изображения")
    source: str = Field(..., max_length=16, description="Источник (stills, wall и т.п.)")


class FilmStillUpdate(BaseModel):
    film_id: Optional[int] = Field(None, description="ID фильма")
    picture_id: Optional[str] = Field(None, max_length=50, description="ID изображения")
    original_url: Optional[str] = Field(None, description="URL оригинального изображения")
    source: Optional[str] = Field(None, max_length=16, description="Источник (stills, wall и т.п.)")


class FilmWatchProviderRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    url: str
    logo: Optional[str] = None
    film_id: int


class FilmWatchProviderCreate(BaseModel):
    film_id: int = Field(..., description="ID фильма")
    name: str = Field(..., max_length=200, description="Название провайдера")
    url: str = Field(..., description="URL провайдера")
    logo: Optional[str] = Field(None, description="URL логотипа")


class FilmWatchProviderUpdate(BaseModel):
    film_id: Optional[int] = Field(None, description="ID фильма")
    name: Optional[str] = Field(None, max_length=200, description="Название провайдера")
    url: Optional[str] = Field(None, description="URL провайдера")
    logo: Optional[str] = Field(None, description="URL логотипа")


class SimilarFilmRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    film_id: int
    similar_film_id: str
    similar_film_title: str
    similar_film_year: Optional[str] = None
    similar_film_genres: Optional[List[str]] = None
    similar_film_poster: Optional[str] = None
    similar_film_rating: Optional[str] = None


class SimilarFilmCreate(BaseModel):
    film_id: int = Field(..., description="ID фильма, к которому относится похожий фильм")
    similar_film_id: str = Field(..., max_length=20, description="Kinopoisk ID похожего фильма")
    similar_film_title: str = Field(..., max_length=500, description="Название похожего фильма")
    similar_film_year: Optional[str] = Field(None, max_length=10, description="Год похожего фильма")
    similar_film_genres: Optional[List[str]] = Field(None, description="Жанры похожего фильма")
    similar_film_poster: Optional[str] = Field(None, description="URL постера похожего фильма")
    similar_film_rating: Optional[str] = Field(None, max_length=10, description="Рейтинг похожего фильма")


class SimilarFilmUpdate(BaseModel):
    film_id: Optional[int] = Field(None, description="ID фильма, к которому относится похожий фильм")
    similar_film_id: Optional[str] = Field(None, max_length=20, description="Kinopoisk ID похожего фильма")
    similar_film_title: Optional[str] = Field(None, max_length=500, description="Название похожего фильма")
    similar_film_year: Optional[str] = Field(None, max_length=10, description="Год похожего фильма")
    similar_film_genres: Optional[List[str]] = Field(None, description="Жанры похожего фильма")
    similar_film_poster: Optional[str] = Field(None, description="URL постера похожего фильма")
    similar_film_rating: Optional[str] = Field(None, max_length=10, description="Рейтинг похожего фильма")
