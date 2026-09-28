from pydantic import BaseModel, Field, ConfigDict

from app.schemas.genre import GenreResponse


class MovieBase(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    director: str = Field(min_length=1, max_length=200)
    release_year: int = Field(ge=1888)


class MovieCreate(MovieBase):
    genre_ids: list[int] = Field(min_length=1)


class MovieUpdate(MovieBase):
    genre_ids: list[int] = Field(min_length=1)


class MovieResponse(MovieBase):
    id: int
    genres: list[GenreResponse] = []

    model_config = ConfigDict(from_attributes=True)