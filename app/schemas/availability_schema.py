from datetime import date, datetime, time

from pydantic import BaseModel, ConfigDict, model_validator


class AvailabilityCreate(BaseModel):
    available_date: date
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def validate_time_range(self):
        if self.start_time >= self.end_time:
            raise ValueError(
                "Start time must be earlier than end time."
            )

        return self


class AvailabilityUpdate(BaseModel):
    available_date: date | None = None
    start_time: time | None = None
    end_time: time | None = None
    is_available: bool | None = None


class AvailabilityResponse(BaseModel):
    availability_id: int
    artist_id: int
    available_date: date
    start_time: time
    end_time: time
    is_available: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )