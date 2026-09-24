from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SqlEnum,
    Integer,
    String,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.models.enums import UserRole
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(150), nullable=False)

    email = Column(
        String(150),
        unique=True,
        nullable=False,
        index=True,
    )

    password_hash = Column(
        String(255),
        nullable=False,
    )

    role = Column(
        SqlEnum(
            UserRole,
            name="user_role",
            values_callable=lambda enum_class: [
                item.value for item in enum_class
            ],
        ),
        nullable=False,
    )

    is_active = Column(
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
    
    artworks = relationship(
        "Artwork",
        back_populates="artist",
        cascade="all, delete-orphan",
    ) 
    
    artist_profile = relationship(
        "ArtistProfile",
        back_populates="artist",
        uselist=False,
        cascade="all, delete-orphan",
    )