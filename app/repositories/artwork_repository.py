from typing import Optional

from sqlalchemy.orm import Session

from app.models.artwork_model import Artwork


def create_artwork(
    db: Session,
    title: str,
    description: str,
    price,
    image_url: Optional[str],
    category: str,
    artist_id: int,
) -> Artwork:
    artwork = Artwork(
        title=title,
        description=description,
        price=price,
        image_url=image_url,
        category=category,
        artist_id=artist_id,
    )

    db.add(artwork)
    db.commit()
    db.refresh(artwork)

    return artwork


def get_artwork_by_id(
    db: Session,
    artwork_id: int,
) -> Optional[Artwork]:
    return (
        db.query(Artwork)
        .filter(Artwork.artwork_id == artwork_id)
        .first()
    )


def get_artworks(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[Artwork]:
    return (
        db.query(Artwork)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_artworks_by_artist_id(
    db: Session,
    artist_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Artwork]:
    return (
        db.query(Artwork)
        .filter(Artwork.artist_id == artist_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_artwork(
    db: Session,
    artwork: Artwork,
    update_data: dict,
) -> Artwork:
    for field, value in update_data.items():
        setattr(artwork, field, value)

    db.commit()
    db.refresh(artwork)

    return artwork


def delete_artwork(
    db: Session,
    artwork: Artwork,
) -> None:
    db.delete(artwork)
    db.commit()