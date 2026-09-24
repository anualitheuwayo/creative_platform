from typing import Optional

from sqlalchemy.orm import Session

from app.models.artist_profile_model import ArtistProfile


def create_artist_profile(
    db: Session,
    artist_id: int,
    bio: str,
    specialization: str,
    location: Optional[str],
    hourly_rate,
    profile_image_url: Optional[str],
) -> ArtistProfile:
    artist_profile = ArtistProfile(
        artist_id=artist_id,
        bio=bio,
        specialization=specialization,
        location=location,
        hourly_rate=hourly_rate,
        profile_image_url=profile_image_url,
    )

    db.add(artist_profile)
    db.commit()
    db.refresh(artist_profile)

    return artist_profile


def get_artist_profile_by_id(
    db: Session,
    artist_profile_id: int,
) -> Optional[ArtistProfile]:
    return (
        db.query(ArtistProfile)
        .filter(
            ArtistProfile.artist_profile_id
            == artist_profile_id
        )
        .first()
    )


def get_artist_profile_by_artist_id(
    db: Session,
    artist_id: int,
) -> Optional[ArtistProfile]:
    return (
        db.query(ArtistProfile)
        .filter(
            ArtistProfile.artist_id == artist_id
        )
        .first()
    )


def get_artist_profiles(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[ArtistProfile]:
    return (
        db.query(ArtistProfile)
        .order_by(
            ArtistProfile.artist_profile_id
        )
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_artist_profile(
    db: Session,
    artist_profile: ArtistProfile,
    update_data: dict,
) -> ArtistProfile:
    for field, value in update_data.items():
        setattr(artist_profile, field, value)

    db.commit()
    db.refresh(artist_profile)

    return artist_profile


def delete_artist_profile(
    db: Session,
    artist_profile: ArtistProfile,
) -> None:
    db.delete(artist_profile)
    db.commit()
    
def update_profile_image_url(
    db: Session,
    artist_profile: ArtistProfile,
    profile_image_url: str,
) -> ArtistProfile:
    artist_profile.profile_image_url = profile_image_url

    db.commit()
    db.refresh(artist_profile)

    return artist_profile    

def update_profile_image_url(
    db: Session,
    artist_profile: ArtistProfile,
    profile_image_url: str,
) -> ArtistProfile:
    artist_profile.profile_image_url = profile_image_url

    db.commit()
    db.refresh(artist_profile)

    return artist_profile