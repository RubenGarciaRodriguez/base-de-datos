from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreResponse


router = APIRouter(
    prefix="/genres",
    tags=["Genres"]
)


@router.post(
    "",
    response_model=GenreResponse,
    status_code=status.HTTP_201_CREATED
)
def create_genre(
    genre: GenreCreate,
    db: Session = Depends(get_db)
):
    existing_genre = db.query(Genre).filter(
        Genre.name == genre.name
    ).first()

    if existing_genre:
        raise HTTPException(
            status_code=400,
            detail="Genre already exists"
        )

    new_genre = Genre(
        name=genre.name
    )

    db.add(new_genre)
    db.commit()
    db.refresh(new_genre)

    return new_genre