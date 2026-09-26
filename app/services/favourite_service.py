from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.favourite_model import Favourite
from app.models.user_model import User
from app.repositories import (
    artwork_repository,
    favourite_repository,
)


def create_favourite(
    db: Session,
    artwork_id: int,
    current_user: User,
) -> Favourite:
    artwork = artwork_repository.get_artwork_by_id(
        db=db,
        artwork_id=artwork_id,
    )

    if not artwork:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artwork not found.",
        )

    existing_favourite = (
        favourite_repository.get_favourite_by_client_and_artwork(
            db=db,
            client_id=current_user.user_id,
            artwork_id=artwork_id,
        )
    )

    if existing_favourite:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Artwork is already in your favourites.",
        )

    return favourite_repository.create_favourite(
        db=db,
        client_id=current_user.user_id,
        artwork_id=artwork_id,
    )


def get_my_favourites(
    db: Session,
    current_user: User,
) -> list[Favourite]:
    return favourite_repository.get_favourites_by_client_id(
        db=db,
        client_id=current_user.user_id,
    )


def delete_my_favourite(
    db: Session,
    favourite_id: int,
    current_user: User,
) -> None:
    favourite = favourite_repository.get_favourite_by_id(
        db=db,
        favourite_id=favourite_id,
    )

    if not favourite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favourite not found.",
        )

    if favourite.client_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only remove your own favourite.",
        )

    favourite_repository.delete_favourite(
        db=db,
        favourite=favourite,
    )