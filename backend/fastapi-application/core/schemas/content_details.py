from typing import Optional, List
from pydantic import BaseModel, ConfigDict


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
