from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import (
    get_current_user,
    require_artist,
)
from app.models.artwork_model import Artwork
from app.models.user_model import User
from app.schemas.artwork_schema import (
    ArtworkCreate,
    ArtworkResponse,
    ArtworkUpdate,
)
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
    new_artwork = Artwork(
        title=artwork_data.title,
        description=artwork_data.description,
        price=artwork_data.price,
        image_url=str(artwork_data.image_url)
        if artwork_data.image_url
        else None,
        category=artwork_data.category,
        artist_id=current_user.user_id,
    )

    db.add(new_artwork)
    db.commit()
    db.refresh(new_artwork)

    return new_artwork


@router.get(
    "",
    response_model=list[ArtworkResponse],
)
def get_artworks(
    db: Session = Depends(get_db),
):
    return db.query(Artwork).order_by(
        Artwork.artwork_id
    ).all()


@router.get(
    "/{artwork_id}",
    response_model=ArtworkResponse,
)
def get_artwork(
    artwork_id: int,
    db: Session = Depends(get_db),
):
    artwork = db.query(Artwork).filter(
        Artwork.artwork_id == artwork_id
    ).first()

    if not artwork:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found.",
        )

    return artwork


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
    artwork = db.query(Artwork).filter(
        Artwork.artwork_id == artwork_id
    ).first()

    if not artwork:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found.",
        )

    if artwork.artist_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own artwork.",
        )

    updates = artwork_data.model_dump(
        exclude_unset=True,
    )

    if "image_url" in updates:
        updates["image_url"] = (
            str(updates["image_url"])
            if updates["image_url"]
            else None
        )

    for field, value in updates.items():
        setattr(artwork, field, value)

    db.commit()
    db.refresh(artwork)

    return artwork


@router.delete(
    "/{artwork_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_artwork(
    artwork_id: int,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    artwork = db.query(Artwork).filter(
        Artwork.artwork_id == artwork_id
    ).first()

    if not artwork:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found.",
        )

    if artwork.artist_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own artwork.",
        )

    db.delete(artwork)
    db.commit()