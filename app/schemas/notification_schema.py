from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import NotificationType


class NotificationCreate(BaseModel):
    recipient_id: int
    notification_type: NotificationType
    message: str = Field(
        min_length=1,
        max_length=1000,
    )


class NotificationResponse(BaseModel):
    notification_id: int
    recipient_id: int
    notification_type: NotificationType
    message: str
    is_read: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )