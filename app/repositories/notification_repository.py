from sqlalchemy.orm import Session

from app.models.enums import NotificationType
from app.models.notification_model import Notification


def create_notification(
    db: Session,
    recipient_id: int,
    notification_type: NotificationType,
    message: str,
) -> Notification:
    notification = Notification(
        recipient_id=recipient_id,
        notification_type=notification_type,
        message=message,
        is_read=False,
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification


def get_notification_by_id(
    db: Session,
    notification_id: int,
) -> Notification | None:
    return db.query(Notification).filter(
        Notification.notification_id == notification_id
    ).first()


def get_notifications_by_recipient_id(
    db: Session,
    recipient_id: int,
) -> list[Notification]:
    return db.query(Notification).filter(
        Notification.recipient_id == recipient_id
    ).order_by(
        Notification.created_at.desc(),
    ).all()


def mark_notification_as_read(
    db: Session,
    notification: Notification,
) -> Notification:
    notification.is_read = True

    db.commit()
    db.refresh(notification)

    return notification