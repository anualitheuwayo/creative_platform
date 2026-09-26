from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Favourite(Base):
    __tablename__ = "favourites"

    __table_args__ = (
        UniqueConstraint(
            "client_id",
            "artwork_id",
            name="uq_favourite_client_artwork",
        ),
    )

    favourite_id = Column(
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

    artwork_id = Column(
        Integer,
        ForeignKey(
            "artworks.artwork_id",
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

    client = relationship(
        "User",
        back_populates="favourites",
    )

    artwork = relationship(
        "Artwork",
        back_populates="favourites",
    )