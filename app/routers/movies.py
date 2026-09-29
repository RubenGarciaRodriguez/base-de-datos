from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.movie import Movie
from app.models.genre import Genre
from app.schemas.movie import MovieCreate, MovieUpdate, MovieResponse


# Router dedicado a las películas.

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


# Devolver una lista de películas

@router.get("", response_model=list[MovieResponse])
def get_movies(db: Session = Depends(get_db)):  # Obtener la sesión
    movies = db.query(Movie).all()  # Consultar las películas

    return movies


@router.get("/{movie_id}", response_model=MovieResponse)
# Crea una ruta como: /movies/1 y FastAPI transformará el resultado
# al formato definido en nuestro schema.
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db)
):  # movie_id debe ser un número entero.

    # Busca en la tabla movies la película cuyo id sea igual a movie_id.
    movie = db.get(Movie, movie_id)

    # Si SQLAlchemy no encuentra ninguna película, movie será None.
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    return movie


@router.post(
    "",
    response_model=MovieResponse,
    status_code=201
)  # 201: código HTTP apropiado para una creación.
def create_movie(movie_data: MovieCreate, db: Session = Depends(get_db)):
    # FastAPI espera que el cuerpo de la petición siga nuestro schema
    genre_ids = movie_data.genre_ids

    # Revisa si hay IDs de género duplicados
    if len(genre_ids) != len(set(genre_ids)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate genre IDs are not allowed"
        )

    # Revisa que todos los géneros existan
    genres = db.query(Genre).filter(Genre.id.in_(genre_ids)).all()

    if len(genres) != len(genre_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more genres not found"
        )

    # Crea el objeto Movie.
    movie = Movie(
        title=movie_data.title,
        director=movie_data.director,
        release_year=movie_data.release_year
    )

    movie.genres = genres  # Asociar los géneros

    db.add(movie)  # Guardar en SQLite
    db.commit()  # Confirma los cambios
    db.refresh(movie)  # Actualiza el objeto

    return movie


@router.put("/{movie_id}", response_model=MovieResponse)
def update_movie(
    movie_id: int,
    movie_data: MovieUpdate,
    db: Session = Depends(get_db)
):
    # Busca la película por su ID
    movie = db.get(Movie, movie_id)

    # Si no existe, devuelve un error 404
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie not found"
        )

    # FastAPI espera que el cuerpo de la petición
    # siga nuestro schema MovieUpdate
    genre_ids = movie_data.genre_ids

    # Revisa si hay IDs de género duplicados
    if len(genre_ids) != len(set(genre_ids)):
        raise HTTPException(
            status_code=400,
            detail="Duplicate genre IDs are not allowed"
        )

    # Revisa que todos los géneros existan
    genres = db.query(Genre).filter(
        Genre.id.in_(genre_ids)
    ).all()

    if len(genres) != len(genre_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more genres not found"
        )

    # Actualiza los datos de la película
    movie.title = movie_data.title
    movie.director = movie_data.director
    movie.release_year = movie_data.release_year

    # Actualiza los géneros asociados a la película
    movie.genres = genres

    # Guarda los cambios en SQLite
    db.commit()

    # Actualiza el objeto con los datos guardados en la base de datos
    db.refresh(movie)

    # Devuelve la película actualizada
    return movie