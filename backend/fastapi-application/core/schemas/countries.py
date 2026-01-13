from pydantic import BaseModel, Field, ConfigDict


class CountryBase(BaseModel):
    name: str = Field(..., max_length=100, description="Название страны")


class CountryCreate(CountryBase):
    pass


class CountryUpdate(BaseModel):
    name: str = Field(..., max_length=100, description="Название страны")


class CountryRead(CountryBase):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
