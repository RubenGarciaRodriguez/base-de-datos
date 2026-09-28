from sqlalchemy import Column, ForeignKey, Integer

from app.database import Base


class MovieGenre(Base):
    __tablename__ = "movie_genres"

    movie_id = Column(
        Integer,
        ForeignKey("movies.id"),
        primary_key=True
    )

    genre_id = Column(
        Integer,
        ForeignKey("genres.id"),
        primary_key=True
    )