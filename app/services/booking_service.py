from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.booking_model import Booking
from app.models.enums import (
    BookingStatus,
    NotificationType,
)
from app.models.user_model import User
from app.repositories import (
    availability_repository,
    booking_repository,
)
from app.schemas.booking_schema import (
    BookingCreate,
    BookingStatusUpdate,
)
from app.services import notification_service


def create_booking(
    db: Session,
    booking_data: BookingCreate,
    current_user: User,
) -> Booking:
    availability = availability_repository.get_availability_by_id(
        db=db,
        availability_id=booking_data.availability_id,
    )

    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found.",
        )

    if not availability.is_available:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Availability slot is no longer available.",
        )

    try:
        booking = booking_repository.create_booking(
            db=db,
            client_id=current_user.user_id,
            artist_id=availability.artist_id,
            availability_id=availability.availability_id,
            message=booking_data.message,
        )

        availability.is_available = False
        db.commit()
        db.refresh(booking)

        notification_service.create_notification(
            db=db,
            recipient_id=booking.artist_id,
            notification_type=NotificationType.BOOKING_CREATED,
            message="You have a new booking request.",
        )

        return booking

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Availability slot is no longer available.",
        )


def get_my_client_bookings(
    db: Session,
    current_user: User,
) -> list[Booking]:
    return booking_repository.get_bookings_by_client_id(
        db=db,
        client_id=current_user.user_id,
    )


def get_my_artist_bookings(
    db: Session,
    current_user: User,
) -> list[Booking]:
    return booking_repository.get_bookings_by_artist_id(
        db=db,
        artist_id=current_user.user_id,
    )


def update_booking_status_as_artist(
    db: Session,
    booking_id: int,
    booking_data: BookingStatusUpdate,
    current_user: User,
) -> Booking:
    booking = booking_repository.get_booking_by_id(
        db=db,
        booking_id=booking_id,
    )

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    if booking.artist_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update bookings assigned to you.",
        )

    allowed_statuses = {
        BookingStatus.ACCEPTED,
        BookingStatus.REJECTED,
        BookingStatus.COMPLETED,
    }

    if booking_data.status not in allowed_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Artists can only set booking status to "
                "accepted, rejected, or completed."
            ),
        )

    if booking.status == BookingStatus.CANCELLED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cancelled bookings cannot be updated.",
        )

    if booking.status == BookingStatus.REJECTED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rejected bookings cannot be updated.",
        )

    if booking.status == BookingStatus.COMPLETED:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Completed bookings cannot be updated.",
        )

    updated_booking = booking_repository.update_booking_status(
        db=db,
        booking=booking,
        status=booking_data.status,
    )

    if booking_data.status == BookingStatus.REJECTED:
        availability = availability_repository.get_availability_by_id(
            db=db,
            availability_id=booking.availability_id,
        )

        if availability:
            availability.is_available = True
            db.commit()
            db.refresh(updated_booking)

    if booking_data.status == BookingStatus.ACCEPTED:
        notification_service.create_notification(
            db=db,
            recipient_id=booking.client_id,
            notification_type=NotificationType.BOOKING_ACCEPTED,
            message="Your booking has been accepted.",
        )

    elif booking_data.status == BookingStatus.REJECTED:
        notification_service.create_notification(
            db=db,
            recipient_id=booking.client_id,
            notification_type=NotificationType.BOOKING_REJECTED,
            message="Your booking has been rejected.",
        )

    return updated_booking


def cancel_my_booking(
    db: Session,
    booking_id: int,
    current_user: User,
) -> Booking:
    booking = booking_repository.get_booking_by_id(
        db=db,
        booking_id=booking_id,
    )

    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found.",
        )

    if booking.client_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only cancel your own bookings.",
        )

    if booking.status not in {
        BookingStatus.PENDING,
        BookingStatus.ACCEPTED,
    }:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This booking cannot be cancelled.",
        )

    cancelled_booking = booking_repository.update_booking_status(
        db=db,
        booking=booking,
        status=BookingStatus.CANCELLED,
    )

    availability = availability_repository.get_availability_by_id(
        db=db,
        availability_id=booking.availability_id,
    )

    if availability:
        availability.is_available = True
        db.commit()
        db.refresh(cancelled_booking)

    notification_service.create_notification(
        db=db,
        recipient_id=booking.artist_id,
        notification_type=NotificationType.BOOKING_CANCELLED,
        message="A client cancelled their booking.",
    )

    return cancelled_booking