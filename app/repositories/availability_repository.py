from datetime import date, time

from sqlalchemy.orm import Session

from app.models.availability_model import Availability


def create_availability(
    db: Session,
    artist_id: int,
    available_date: date,
    start_time: time,
    end_time: time,
) -> Availability:
    availability = Availability(
        artist_id=artist_id,
        available_date=available_date,
        start_time=start_time,
        end_time=end_time,
    )

    db.add(availability)
    db.commit()
    db.refresh(availability)

    return availability


def get_availability_by_id(
    db: Session,
    availability_id: int,
) -> Availability | None:
    return db.query(Availability).filter(
        Availability.availability_id == availability_id
    ).first()


def get_availabilities_by_artist_id(
    db: Session,
    artist_id: int,
) -> list[Availability]:
    return db.query(Availability).filter(
        Availability.artist_id == artist_id
    ).order_by(
        Availability.available_date.asc(),
        Availability.start_time.asc(),
    ).all()


def get_available_slots_by_artist_id(
    db: Session,
    artist_id: int,
) -> list[Availability]:
    return db.query(Availability).filter(
        Availability.artist_id == artist_id,
        Availability.is_available.is_(True),
    ).order_by(
        Availability.available_date.asc(),
        Availability.start_time.asc(),
    ).all()


def update_availability(
    db: Session,
    availability: Availability,
    update_data: dict,
) -> Availability:
    for field, value in update_data.items():
        setattr(availability, field, value)

    db.commit()
    db.refresh(availability)

    return availability


def delete_availability(
    db: Session,
    availability: Availability,
) -> None:
    db.delete(availability)
    db.commit()