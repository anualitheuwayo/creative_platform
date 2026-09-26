from sqlalchemy import (
    Column,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.enums import BookingStatus
from database import Base


class Booking(Base):
    __tablename__ = "bookings"


    booking_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    client_id = Column(
        Integer,
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )


    artist_id = Column(
        Integer,
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )


    availability_id = Column(
        Integer,
        ForeignKey(
            "availabilities.availability_id",
            ondelete="RESTRICT",
        ),
        nullable=False,
        unique=True,
        index=True,
    )


    message = Column(
        String(1000),
        nullable=True,
    )


    status = Column(
        SqlEnum(
            BookingStatus,
            name="booking_status",
        ),
        nullable=False,
        default=BookingStatus.PENDING,
        index=True,
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


    client = relationship(
        "User",
        foreign_keys=[client_id],
        back_populates="client_bookings",
    )


    artist = relationship(
        "User",
        foreign_keys=[artist_id],
        back_populates="artist_bookings",
    )


    availability = relationship(
        "Availability",
        back_populates="booking",
    )