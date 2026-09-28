from fastapi import FastAPI

from app.database import Base, engine
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Movie API",
    description="API REST para gestionar películas y géneros",
    version="1.0.0"
)


@app.get("/")
def read_root():
    return {
        "message": "Movie API funcionando"
    }