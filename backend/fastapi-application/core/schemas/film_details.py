from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict

class FilmStillBase(BaseModel):
    film_id: int = Field(..., description="ID фильма")
    picture_id: str = Field(..., max_length=50, description="ID изображения")
    original_url: str = Field(..., description="URL оригинального изображения")
    source: str = Field(..., max_length=16, description="Источник (stills, wall и т.п.)")


class FilmStillCreate(FilmStillBase):
    pass


class FilmStillUpdate(BaseModel):
    film_id: Optional[int] = Field(None, description="ID фильма")
    picture_id: Optional[str] = Field(None, max_length=50, description="ID изображения")
    original_url: Optional[str] = Field(None, description="URL оригинального изображения")
    source: Optional[str] = Field(None, max_length=16, description="Источник (stills, wall и т.п.)")


class FilmStillRead(FilmStillBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class FilmWatchProviderOptional(BaseModel):
    logo: Optional[str] = Field(None, description="URL логотипа")


class FilmWatchProviderBase(FilmWatchProviderOptional):
    film_id: int = Field(..., description="ID фильма")
    name: str = Field(..., max_length=200, description="Название провайдера")
    url: str = Field(..., description="URL провайдера")


class FilmWatchProviderCreate(FilmWatchProviderBase):
    pass


class FilmWatchProviderUpdate(FilmWatchProviderOptional):
    film_id: Optional[int] = Field(None, description="ID фильма")
    name: Optional[str] = Field(None, max_length=200, description="Название провайдера")
    url: Optional[str] = Field(None, description="URL провайдера")


class FilmWatchProviderRead(FilmWatchProviderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class SimilarFilmOptional(BaseModel):
    similar_film_year: Optional[str] = Field(None, max_length=10, description="Год похожего фильма")
    similar_film_genres: Optional[List[str]] = Field(None, description="Жанры похожего фильма")
    similar_film_poster: Optional[str] = Field(None, description="URL постера похожего фильма")
    similar_film_rating: Optional[str] = Field(None, max_length=10, description="Рейтинг похожего фильма")


class SimilarFilmBase(SimilarFilmOptional):
    film_id: int = Field(..., description="ID фильма, к которому относится похожий фильм")
    similar_film_id: str = Field(..., max_length=20, description="Kinopoisk ID похожего фильма")
    similar_film_title: str = Field(..., max_length=500, description="Название похожего фильма")


class SimilarFilmCreate(SimilarFilmBase):
    pass


class SimilarFilmUpdate(SimilarFilmOptional):
    film_id: Optional[int] = Field(None, description="ID фильма, к которому относится похожий фильм")
    similar_film_id: Optional[str] = Field(None, max_length=20, description="Kinopoisk ID похожего фильма")
    similar_film_title: Optional[str] = Field(None, max_length=500, description="Название похожего фильма")


class SimilarFilmRead(SimilarFilmBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
