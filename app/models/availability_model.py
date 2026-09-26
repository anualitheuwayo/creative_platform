from sqlalchemy import (
    Boolean,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    Time,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Availability(Base):
    __tablename__ = "availabilities"


    availability_id = Column(
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
        nullable=False,
        index=True,
    )


    available_date = Column(
        Date,
        nullable=False,
        index=True,
    )


    start_time = Column(
        Time,
        nullable=False,
    )


    end_time = Column(
        Time,
        nullable=False,
    )


    is_available = Column(
        Boolean,
        nullable=False,
        default=True,
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
        back_populates="availabilities",
    )
    
    booking = relationship(
    "Booking",
    back_populates="availability",
    uselist=False,
)