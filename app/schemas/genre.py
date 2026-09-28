from pydantic import BaseModel, Field, ConfigDict


class GenreBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class GenreCreate(GenreBase):
    pass


class GenreUpdate(GenreBase):
    pass


class GenreResponse(GenreBase):
    id: int

    model_config = ConfigDict(from_attributes=True)