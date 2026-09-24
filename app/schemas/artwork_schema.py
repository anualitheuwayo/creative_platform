from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ArtworkCreate(BaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str = Field(
        min_length=10,
    )

    price: Decimal = Field(
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    image_url: Optional[HttpUrl] = None

    category: str = Field(
        min_length=2,
        max_length=100,
    )


class ArtworkUpdate(BaseModel):
    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: Optional[str] = Field(
        default=None,
        min_length=10,
    )

    price: Optional[Decimal] = Field(
        default=None,
        gt=0,
        max_digits=10,
        decimal_places=2,
    )

    image_url: Optional[HttpUrl] = None

    category: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    is_available: Optional[bool] = None


class ArtworkResponse(BaseModel):
    artwork_id: int
    title: str
    description: str
    price: Decimal
    image_url: Optional[str]
    category: str
    is_available: bool
    artist_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )