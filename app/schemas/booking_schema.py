from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import BookingStatus


class BookingCreate(BaseModel):
    availability_id: int
    message: str | None = Field(
        default=None,
        max_length=1000,
    )


class BookingStatusUpdate(BaseModel):
    status: BookingStatus


class BookingResponse(BaseModel):
    booking_id: int
    client_id: int
    artist_id: int
    availability_id: int
    message: str | None
    status: BookingStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )