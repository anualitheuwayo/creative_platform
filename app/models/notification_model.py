from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum as SqlEnum,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.enums import NotificationType
from database import Base


class Notification(Base):
    __tablename__ = "notifications"


    notification_id = Column(
        Integer,
        primary_key=True,
        index=True,
    )


    recipient_id = Column(
        Integer,
        ForeignKey(
            "users.user_id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )


    notification_type = Column(
        SqlEnum(
            NotificationType,
            name="notification_type",
        ),
        nullable=False,
        index=True,
    )


    message = Column(
        Text,
        nullable=False,
    )


    is_read = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True,
    )


    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )


    recipient = relationship(
        "User",
        back_populates="notifications",
    )