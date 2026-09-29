from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    release_year = Column(Integer, nullable=False)

    genres = relationship(
        "Genre",
        secondary="movie_genres",
        back_populates="movies"
    )