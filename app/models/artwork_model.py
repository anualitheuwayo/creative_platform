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


class Artwork(Base):
    __tablename__ = "artworks"

    artwork_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String(200),
        nullable=False,
    )

    description = Column(
        Text,
        nullable=False,
    )

    price = Column(
        Numeric(10, 2),
        nullable=False,
    )

    image_url = Column(
        String(500),
        nullable=True,
    )

    category = Column(
        String(100),
        nullable=False,
    )

    is_available = Column(
        Boolean,
        nullable=False,
        default=True,
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
        back_populates="artworks",
    )