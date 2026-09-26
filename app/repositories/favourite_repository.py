from typing import Optional

from sqlalchemy.orm import Session

from app.models.favourite_model import Favourite


def create_favourite(
    db: Session,
    client_id: int,
    artwork_id: int,
) -> Favourite:
    favourite = Favourite(
        client_id=client_id,
        artwork_id=artwork_id,
    )

    db.add(favourite)
    db.commit()
    db.refresh(favourite)

    return favourite


def get_favourite_by_id(
    db: Session,
    favourite_id: int,
) -> Optional[Favourite]:
    return (
        db.query(Favourite)
        .filter(
            Favourite.favourite_id == favourite_id
        )
        .first()
    )


def get_favourite_by_client_and_artwork(
    db: Session,
    client_id: int,
    artwork_id: int,
) -> Optional[Favourite]:
    return (
        db.query(Favourite)
        .filter(
            Favourite.client_id == client_id,
            Favourite.artwork_id == artwork_id,
        )
        .first()
    )


def get_favourites_by_client_id(
    db: Session,
    client_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Favourite]:
    return (
        db.query(Favourite)
        .filter(
            Favourite.client_id == client_id
        )
        .order_by(
            Favourite.favourite_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def delete_favourite(
    db: Session,
    favourite: Favourite,
) -> None:
    db.delete(favourite)
    db.commit()