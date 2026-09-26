import shutil
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.models.artist_profile_model import ArtistProfile
from app.models.user_model import User
from app.repositories import artist_profile_repository
from app.schemas.artist_profile_schema import (
    ArtistProfileCreate,
    ArtistProfileUpdate,
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
    "uploads/profile-images"
)


def mask_public_phone_number(
    artist_profile: ArtistProfile,
) -> ArtistProfile:
    """
    Hides the phone number for public responses when the Artist
    has disabled phone-number visibility.

    This changes only the in-memory SQLAlchemy object returned
    to FastAPI; it does not call db.commit(), so the stored
    database value remains unchanged.
    """
    if not artist_profile.show_phone_number:
        artist_profile.phone_number = None

    return artist_profile


def create_artist_profile(
    db: Session,
    profile_data: ArtistProfileCreate,
    current_user: User,
) -> ArtistProfile:
    existing_profile = (
        artist_profile_repository.get_artist_profile_by_artist_id(
            db=db,
            artist_id=current_user.user_id,
        )
    )

    if existing_profile:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Artist profile already exists.",
        )

    profile_image_url = (
        str(profile_data.profile_image_url)
        if profile_data.profile_image_url
        else None
    )

    return artist_profile_repository.create_artist_profile(
        db=db,
        artist_id=current_user.user_id,
        bio=profile_data.bio,
        specialization=profile_data.specialization,
        location=profile_data.location,
        hourly_rate=profile_data.hourly_rate,
        profile_image_url=profile_image_url,
        phone_number=profile_data.phone_number,
        show_phone_number=profile_data.show_phone_number,
    )


def get_artist_profiles(
    db: Session,
) -> list[ArtistProfile]:
    artist_profiles = (
        artist_profile_repository.get_artist_profiles(
            db=db,
        )
    )

    return [
        mask_public_phone_number(
            artist_profile=artist_profile,
        )
        for artist_profile in artist_profiles
    ]


def get_artist_profile(
    db: Session,
    artist_profile_id: int,
) -> ArtistProfile:
    artist_profile = (
        artist_profile_repository.get_artist_profile_by_id(
            db=db,
            artist_profile_id=artist_profile_id,
        )
    )

    if not artist_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist profile not found.",
        )

    return mask_public_phone_number(
        artist_profile=artist_profile,
    )


def get_my_artist_profile(
    db: Session,
    current_user: User,
) -> ArtistProfile:
    artist_profile = (
        artist_profile_repository.get_artist_profile_by_artist_id(
            db=db,
            artist_id=current_user.user_id,
        )
    )

    if not artist_profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artist profile not found.",
        )

    return artist_profile


def update_my_artist_profile(
    db: Session,
    profile_data: ArtistProfileUpdate,
    current_user: User,
) -> ArtistProfile:
    artist_profile = get_my_artist_profile(
        db=db,
        current_user=current_user,
    )

    updates = profile_data.model_dump(
        exclude_unset=True,
    )

    if "profile_image_url" in updates:
        updates["profile_image_url"] = (
            str(updates["profile_image_url"])
            if updates["profile_image_url"]
            else None
        )

    return artist_profile_repository.update_artist_profile(
        db=db,
        artist_profile=artist_profile,
        update_data=updates,
    )


def delete_my_artist_profile(
    db: Session,
    current_user: User,
) -> None:
    artist_profile = get_my_artist_profile(
        db=db,
        current_user=current_user,
    )

    artist_profile_repository.delete_artist_profile(
        db=db,
        artist_profile=artist_profile,
    )


def upload_my_profile_image(
    db: Session,
    image: UploadFile,
    current_user: User,
) -> ArtistProfile:
    artist_profile = get_my_artist_profile(
        db=db,
        current_user=current_user,
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

    profile_image_url = (
        f"/uploads/profile-images/{filename}"
    )

    return (
        artist_profile_repository.update_profile_image_url(
            db=db,
            artist_profile=artist_profile,
            profile_image_url=profile_image_url,
        )
    )