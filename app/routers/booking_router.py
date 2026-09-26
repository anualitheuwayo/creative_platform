from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import (
    require_artist,
    require_client,
)
from app.models.user_model import User
from app.schemas.booking_schema import (
    BookingCreate,
    BookingResponse,
    BookingStatusUpdate,
)
from app.services import booking_service
from database import get_db


router = APIRouter(
    prefix="/api/v1/bookings",
    tags=["Bookings"],
)


@router.post(
    "/",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_booking(
    booking_data: BookingCreate,
    current_user: User = Depends(require_client),
    db: Session = Depends(get_db),
):
    return booking_service.create_booking(
        db=db,
        booking_data=booking_data,
        current_user=current_user,
    )


@router.get(
    "/me/client",
    response_model=list[BookingResponse],
)
def get_my_client_bookings(
    current_user: User = Depends(require_client),
    db: Session = Depends(get_db),
):
    return booking_service.get_my_client_bookings(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/me/artist",
    response_model=list[BookingResponse],
)
def get_my_artist_bookings(
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return booking_service.get_my_artist_bookings(
        db=db,
        current_user=current_user,
    )


@router.patch(
    "/{booking_id}/status",
    response_model=BookingResponse,
)
def update_booking_status_as_artist(
    booking_id: int,
    booking_data: BookingStatusUpdate,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return booking_service.update_booking_status_as_artist(
        db=db,
        booking_id=booking_id,
        booking_data=booking_data,
        current_user=current_user,
    )


@router.patch(
    "/{booking_id}/cancel",
    response_model=BookingResponse,
)
def cancel_my_booking(
    booking_id: int,
    current_user: User = Depends(require_client),
    db: Session = Depends(get_db),
):
    return booking_service.cancel_my_booking(
        db=db,
        booking_id=booking_id,
        current_user=current_user,
    )