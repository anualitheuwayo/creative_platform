import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.artwork_model import Artwork
from app.models.user_model import User
from app.repositories import artwork_repository
from app.schemas.artwork_schema import (
    ArtworkCreate,
    ArtworkUpdate,
)


ALLOWED_IMAGE_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


ALLOWED_IMAGE_SUFFIXES = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


UPLOAD_DIRECTORY = Path(
    "uploads/artwork-images"
)


def create_artwork(
    db: Session,
    artwork_data: ArtworkCreate,
    current_user: User,
) -> Artwork:
    image_url = (
        str(artwork_data.image_url)
        if artwork_data.image_url
        else None
    )

    return artwork_repository.create_artwork(
        db=db,
        title=artwork_data.title,
        description=artwork_data.description,
        price=artwork_data.price,
        image_url=image_url,
        category=artwork_data.category,
        artist_id=current_user.user_id,
    )


def get_artworks(
    db: Session,
) -> list[Artwork]:
    return artwork_repository.get_artworks(
        db=db,
    )


def get_artwork(
    db: Session,
    artwork_id: int,
) -> Artwork:
    artwork = artwork_repository.get_artwork_by_id(
        db=db,
        artwork_id=artwork_id,
    )

    if not artwork:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found.",
        )

    return artwork


def update_artwork(
    db: Session,
    artwork_id: int,
    artwork_data: ArtworkUpdate,
    current_user: User,
) -> Artwork:
    artwork = get_artwork(
        db=db,
        artwork_id=artwork_id,
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

    return artwork_repository.update_artwork(
        db=db,
        artwork=artwork,
        update_data=updates,
    )


def delete_artwork(
    db: Session,
    artwork_id: int,
    current_user: User,
) -> None:
    artwork = get_artwork(
        db=db,
        artwork_id=artwork_id,
    )

    if artwork.artist_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own artwork.",
        )

    artwork_repository.delete_artwork(
        db=db,
        artwork=artwork,
    )


def upload_artwork_image(
    db: Session,
    artwork_id: int,
    image: UploadFile,
    current_user: User,
) -> Artwork:
    artwork = get_artwork(
        db=db,
        artwork_id=artwork_id,
    )

    if artwork.artist_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "You can only upload an image "
                "for your own artwork."
            ),
        )

    if image.content_type not in ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Only JPEG, PNG, and WEBP "
                "images are allowed."
            ),
        )

    original_suffix = Path(
        image.filename or ""
    ).suffix.lower()

    if original_suffix not in ALLOWED_IMAGE_SUFFIXES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file extension.",
        )

    UPLOAD_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    filename = f"{uuid4().hex}{original_suffix}"

    file_path = UPLOAD_DIRECTORY / filename

    with file_path.open("wb") as output_file:
        shutil.copyfileobj(
            image.file,
            output_file,
        )

    image_url = (
        f"/uploads/artwork-images/{filename}"
    )

    return artwork_repository.update_artwork_image_url(
        db=db,
        artwork=artwork,
        image_url=image_url,
    )