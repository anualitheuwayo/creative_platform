from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class ArtistProfile(Base):
    __tablename__ = "artist_profiles"

    artist_profile_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    artist_id = Column(
        Integer,
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
        index=True,
    )

    bio = Column(
        Text,
        nullable=False,
    )

    specialization = Column(
        String(150),
        nullable=False,
    )

    location = Column(
        String(150),
        nullable=True,
    )

    hourly_rate = Column(
        Numeric(10, 2),
        nullable=True,
    )

    profile_image_url = Column(
        String(500),
        nullable=True,
    )

    is_verified = Column(
        Boolean,
        nullable=False,
        default=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    artist = relationship(
        "User",
        back_populates="artist_profile",
    )