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
