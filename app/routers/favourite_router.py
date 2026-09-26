from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import require_client
from app.models.user_model import User
from app.schemas.favourite_schema import FavouriteResponse
from app.services import favourite_service
from database import get_db


router = APIRouter(
    prefix="/api/v1/favourites",
    tags=["Favourites"],
)


@router.post(
    "/artworks/{artwork_id}",
    response_model=FavouriteResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_favourite(
    artwork_id: int,
    current_user: User = Depends(require_client),
    db: Session = Depends(get_db),
):
    return favourite_service.create_favourite(
        db=db,
        artwork_id=artwork_id,
        current_user=current_user,
    )


@router.get(
    "/me",
    response_model=list[FavouriteResponse],
)
def get_my_favourites(
    current_user: User = Depends(require_client),
    db: Session = Depends(get_db),
):
    return favourite_service.get_my_favourites(
        db=db,
        current_user=current_user,
    )


@router.delete(
    "/{favourite_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_favourite(
    favourite_id: int,
    current_user: User = Depends(require_client),
    db: Session = Depends(get_db),
):
    favourite_service.delete_my_favourite(
        db=db,
        favourite_id=favourite_id,
        current_user=current_user,
    )