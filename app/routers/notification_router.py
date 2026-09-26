from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import get_current_user
from app.models.user_model import User
from app.schemas.notification_schema import NotificationResponse
from app.services import notification_service
from database import get_db


router = APIRouter(
    prefix="/api/v1/notifications",
    tags=["Notifications"],
)


@router.get(
    "/me",
    response_model=list[NotificationResponse],
)
def get_my_notifications(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return notification_service.get_my_notifications(
        db=db,
        current_user=current_user,
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse,
)
def mark_my_notification_as_read(
    notification_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return notification_service.mark_my_notification_as_read(
        db=db,
        notification_id=notification_id,
        current_user=current_user,
    )