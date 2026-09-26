from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import require_artist
from app.models.user_model import User
from app.schemas.availability_schema import (
    AvailabilityCreate,
    AvailabilityResponse,
    AvailabilityUpdate,
)
from app.services import availability_service
from database import get_db


router = APIRouter(
    prefix="/api/v1/availabilities",
    tags=["Availabilities"],
)


@router.post(
    "/",
    response_model=AvailabilityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_availability(
    availability_data: AvailabilityCreate,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return availability_service.create_availability(
        db=db,
        availability_data=availability_data,
        current_user=current_user,
    )


@router.get(
    "/me",
    response_model=list[AvailabilityResponse],
)
def get_my_availabilities(
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return availability_service.get_my_availabilities(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/artist/{artist_id}",
    response_model=list[AvailabilityResponse],
)
def get_artist_available_slots(
    artist_id: int,
    db: Session = Depends(get_db),
):
    return availability_service.get_artist_available_slots(
        db=db,
        artist_id=artist_id,
    )


@router.patch(
    "/{availability_id}",
    response_model=AvailabilityResponse,
)
def update_my_availability(
    availability_id: int,
    availability_data: AvailabilityUpdate,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return availability_service.update_my_availability(
        db=db,
        availability_id=availability_id,
        availability_data=availability_data,
        current_user=current_user,
    )


@router.delete(
    "/{availability_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_availability(
    availability_id: int,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    availability_service.delete_my_availability(
        db=db,
        availability_id=availability_id,
        current_user=current_user,
    )