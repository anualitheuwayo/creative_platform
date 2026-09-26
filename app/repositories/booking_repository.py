from sqlalchemy.orm import Session

from app.models.booking_model import Booking
from app.models.enums import BookingStatus


def create_booking(
    db: Session,
    client_id: int,
    artist_id: int,
    availability_id: int,
    message: str | None,
) -> Booking:
    booking = Booking(
        client_id=client_id,
        artist_id=artist_id,
        availability_id=availability_id,
        message=message,
        status=BookingStatus.PENDING,
    )

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return booking


def get_booking_by_id(
    db: Session,
    booking_id: int,
) -> Booking | None:
    return db.query(Booking).filter(
        Booking.booking_id == booking_id
    ).first()


def get_bookings_by_client_id(
    db: Session,
    client_id: int,
) -> list[Booking]:
    return db.query(Booking).filter(
        Booking.client_id == client_id
    ).order_by(
        Booking.created_at.desc(),
    ).all()


def get_bookings_by_artist_id(
    db: Session,
    artist_id: int,
) -> list[Booking]:
    return db.query(Booking).filter(
        Booking.artist_id == artist_id
    ).order_by(
        Booking.created_at.desc(),
    ).all()


def update_booking_status(
    db: Session,
    booking: Booking,
    status: BookingStatus,
) -> Booking:
    booking.status = status

    db.commit()
    db.refresh(booking)

    return booking