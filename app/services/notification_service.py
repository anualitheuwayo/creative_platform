from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import NotificationType
from app.models.notification_model import Notification
from app.models.user_model import User
from app.repositories import notification_repository


def create_notification(
    db: Session,
    recipient_id: int,
    notification_type: NotificationType,
    message: str,
) -> Notification:
    return notification_repository.create_notification(
        db=db,
        recipient_id=recipient_id,
        notification_type=notification_type,
        message=message,
    )


def get_my_notifications(
    db: Session,
    current_user: User,
) -> list[Notification]:
    return notification_repository.get_notifications_by_recipient_id(
        db=db,
        recipient_id=current_user.user_id,
    )


def mark_my_notification_as_read(
    db: Session,
    notification_id: int,
    current_user: User,
) -> Notification:
    notification = notification_repository.get_notification_by_id(
        db=db,
        notification_id=notification_id,
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found.",
        )

    if notification.recipient_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own notifications.",
        )

    return notification_repository.mark_notification_as_read(
        db=db,
        notification=notification,
    )