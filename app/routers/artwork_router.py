from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import (
    get_current_user,
    require_artist,
)
from app.models.user_model import User
from app.schemas.artwork_schema import (
    ArtworkCreate,
    ArtworkResponse,
    ArtworkUpdate,
)
from app.services import artwork_service
from database import get_db


router = APIRouter(
    prefix="/api/v1/artworks",
    tags=["Artworks"],
)


@router.post(
    "",
    response_model=ArtworkResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_artwork(
    artwork_data: ArtworkCreate,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return artwork_service.create_artwork(
        db=db,
        artwork_data=artwork_data,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[ArtworkResponse],
)
def get_artworks(
    db: Session = Depends(get_db),
):
    return artwork_service.get_artworks(
        db=db,
    )


@router.get(
    "/{artwork_id}",
    response_model=ArtworkResponse,
)
def get_artwork(
    artwork_id: int,
    db: Session = Depends(get_db),
):
    return artwork_service.get_artwork(
        db=db,
        artwork_id=artwork_id,
    )


@router.patch(
    "/{artwork_id}",
    response_model=ArtworkResponse,
)
def update_artwork(
    artwork_id: int,
    artwork_data: ArtworkUpdate,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return artwork_service.update_artwork(
        db=db,
        artwork_id=artwork_id,
        artwork_data=artwork_data,
        current_user=current_user,
    )


@router.delete(
    "/{artwork_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_artwork(
    artwork_id: int,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    artwork_service.delete_artwork(
        db=db,
        artwork_id=artwork_id,
        current_user=current_user,
    )