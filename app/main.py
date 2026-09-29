from fastapi import FastAPI

from app.database import Base, engine
from app.models.movie import Movie
from app.models.genre import Genre
from app.models.movie_genre import MovieGenre
from app.routers.movies import router as movies_router
from app.routers.genres import router as genres_router


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Movie API",
    description="API REST para gestionar películas y géneros",
    version="1.0.0"
)


app.include_router(movies_router) #conecta movies.py con FastAPI.
app.include_router(genres_router)


@app.get("/")
def read_root():
    return {
        "message": "Movie API funcionando"
    }