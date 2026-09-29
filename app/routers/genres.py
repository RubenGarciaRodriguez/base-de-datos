from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate, GenreResponse


# Router dedicado a los géneros.
router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


# Devolver una lista de géneros.
@router.get("", response_model=list[GenreResponse])
def get_genres(db: Session = Depends(get_db)):
    # Consulta todos los géneros de la base de datos.
    genres = db.query(Genre).all()

    return genres


# Devolver un género concreto mediante su ID.
@router.get("/{genre_id}", response_model=GenreResponse)
def get_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):
    # Busca el género por su ID.
    genre = db.get(Genre, genre_id)

    # Si no existe, devuelve un error 404.
    if genre is None:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    return genre


# Crear un nuevo género.
@router.post(
    "",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED
)  # 201: código HTTP apropiado para una creación.
def create_genre(
    genre_data: GenreCreate,
    db: Session = Depends(get_db)
):
    # Comprueba si ya existe un género con el mismo nombre.
    existing_genre = db.query(Genre).filter(
        Genre.name == genre_data.name
    ).first()

    # Si ya existe, devuelve un error 400.
    if existing_genre:
        raise HTTPException(
            status_code=400,
            detail="Genre already exists"
        )

    # Crea el objeto Genre.
    genre = Genre(
        name=genre_data.name
    )

    # Guarda el género en SQLite.
    db.add(genre)

    # Confirma los cambios en la base de datos.
    db.commit()

    # Actualiza el objeto con los datos generados por la base de datos,
    # como su ID.
    db.refresh(genre)

    return genre


# Actualizar un género existente.
@router.put("/{genre_id}", response_model=GenreResponse)
def update_genre(
    genre_id: int,
    genre_data: GenreUpdate,
    db: Session = Depends(get_db)
):
    # Busca el género que queremos actualizar.
    genre = db.get(Genre, genre_id)

    # Si no existe, devuelve un error 404.
    if genre is None:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    # Comprueba si ya existe otro género con el mismo nombre.
    existing_genre = db.query(Genre).filter(
        Genre.name == genre_data.name,
        Genre.id != genre_id
    ).first()

    # Si existe otro género con ese nombre, devuelve un error 400.
    if existing_genre:
        raise HTTPException(
            status_code=400,
            detail="Genre already exists"
        )

    # Actualiza el nombre del género.
    genre.name = genre_data.name

    # Guarda los cambios en SQLite.
    db.commit()

    # Actualiza el objeto con los datos guardados.
    db.refresh(genre)

    # Devuelve el género actualizado.
    return genre


# Eliminar un género existente.
@router.delete("/{genre_id}", status_code=204)
def delete_genre(
    genre_id: int,
    db: Session = Depends(get_db)
):
    # Busca el género por su ID.
    genre = db.get(Genre, genre_id)

    # Si no existe, devuelve un error 404.
    if genre is None:
        raise HTTPException(
            status_code=404,
            detail="Genre not found"
        )

    # Elimina las relaciones entre este género y sus películas
    # de la tabla intermedia movie_genres.
    genre.movies = []

    # Elimina el género de la base de datos.
    db.delete(genre)

    # Confirma los cambios en SQLite.
    db.commit()