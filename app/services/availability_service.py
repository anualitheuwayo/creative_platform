from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.availability_model import Availability
from app.models.user_model import User
from app.repositories import availability_repository
from app.schemas.availability_schema import (
    AvailabilityCreate,
    AvailabilityUpdate,
)


def create_availability(
    db: Session,
    availability_data: AvailabilityCreate,
    current_user: User,
) -> Availability:
    if availability_data.available_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Availability date cannot be in the past.",
        )

    return availability_repository.create_availability(
        db=db,
        artist_id=current_user.user_id,
        available_date=availability_data.available_date,
        start_time=availability_data.start_time,
        end_time=availability_data.end_time,
    )


def get_my_availabilities(
    db: Session,
    current_user: User,
) -> list[Availability]:
    return availability_repository.get_availabilities_by_artist_id(
        db=db,
        artist_id=current_user.user_id,
    )


def get_artist_available_slots(
    db: Session,
    artist_id: int,
) -> list[Availability]:
    return availability_repository.get_available_slots_by_artist_id(
        db=db,
        artist_id=artist_id,
    )


def update_my_availability(
    db: Session,
    availability_id: int,
    availability_data: AvailabilityUpdate,
    current_user: User,
) -> Availability:
    availability = availability_repository.get_availability_by_id(
        db=db,
        availability_id=availability_id,
    )

    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found.",
        )

    if availability.artist_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own availability slots.",
        )

    update_data = availability_data.model_dump(
        exclude_unset=True,
    )

    final_date = update_data.get(
        "available_date",
        availability.available_date,
    )

    final_start_time = update_data.get(
        "start_time",
        availability.start_time,
    )

    final_end_time = update_data.get(
        "end_time",
        availability.end_time,
    )

    if final_date < date.today():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Availability date cannot be in the past.",
        )

    if final_start_time >= final_end_time:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start time must be earlier than end time.",
        )

    return availability_repository.update_availability(
        db=db,
        availability=availability,
        update_data=update_data,
    )


def delete_my_availability(
    db: Session,
    availability_id: int,
    current_user: User,
) -> None:
    availability = availability_repository.get_availability_by_id(
        db=db,
        availability_id=availability_id,
    )

    if not availability:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found.",
        )

    if availability.artist_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own availability slots.",
        )

    availability_repository.delete_availability(
        db=db,
        availability=availability,
    )