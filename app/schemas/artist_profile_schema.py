from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ArtistProfileCreate(BaseModel):
    bio: str = Field(
        min_length=10,
        max_length=2000,
    )

    specialization: str = Field(
        min_length=2,
        max_length=150,
    )

    location: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    hourly_rate: Optional[Decimal] = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    profile_image_url: Optional[str] = Field(
        default=None,
        max_length=500,
    )


class ArtistProfileUpdate(BaseModel):
    bio: Optional[str] = Field(
        default=None,
        min_length=10,
        max_length=2000,
    )

    specialization: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    location: Optional[str] = Field(
        default=None,
        max_length=150,
    )

    hourly_rate: Optional[Decimal] = Field(
        default=None,
        ge=0,
        max_digits=10,
        decimal_places=2,
    )

    profile_image_url: Optional[str] = Field(
        default=None,
        max_length=500,
    )


class ArtistProfileResponse(BaseModel):
    artist_profile_id: int
    artist_id: int
    bio: str
    specialization: str
    location: Optional[str]
    hourly_rate: Optional[Decimal]
    profile_image_url: Optional[str]
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )