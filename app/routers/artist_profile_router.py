from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    status,
)

from sqlalchemy.orm import Session

from app.dependencies.auth_dependency import require_artist
from app.models.user_model import User
from app.schemas.artist_profile_schema import (
    ArtistProfileCreate,
    ArtistProfileResponse,
    ArtistProfileUpdate,
)
from app.services import artist_profile_service
from database import get_db


router = APIRouter(
    prefix="/api/v1/artist-profiles",
    tags=["Artist Profiles"],
)


@router.post(
    "",
    response_model=ArtistProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_artist_profile(
    profile_data: ArtistProfileCreate,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return artist_profile_service.create_artist_profile(
        db=db,
        profile_data=profile_data,
        current_user=current_user,
    )


@router.get(
    "",
    response_model=list[ArtistProfileResponse],
)
def get_artist_profiles(
    db: Session = Depends(get_db),
):
    return artist_profile_service.get_artist_profiles(
        db=db,
    )


@router.get(
    "/me",
    response_model=ArtistProfileResponse,
)
def get_my_artist_profile(
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return artist_profile_service.get_my_artist_profile(
        db=db,
        current_user=current_user,
    )
    
@router.post(
    "/me/image",
    response_model=ArtistProfileResponse,
)
def upload_my_profile_image(
    image: UploadFile = File(...),
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return artist_profile_service.upload_my_profile_image(
        db=db,
        image=image,
        current_user=current_user,
    )    


@router.patch(
    "/me",
    response_model=ArtistProfileResponse,
)
def update_my_artist_profile(
    profile_data: ArtistProfileUpdate,
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    return artist_profile_service.update_my_artist_profile(
        db=db,
        profile_data=profile_data,
        current_user=current_user,
    )


@router.delete(
    "/me",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_my_artist_profile(
    current_user: User = Depends(require_artist),
    db: Session = Depends(get_db),
):
    artist_profile_service.delete_my_artist_profile(
        db=db,
        current_user=current_user,
    )


@router.get(
    "/{artist_profile_id}",
    response_model=ArtistProfileResponse,
)
def get_artist_profile(
    artist_profile_id: int,
    db: Session = Depends(get_db),
):
    return artist_profile_service.get_artist_profile(
        db=db,
        artist_profile_id=artist_profile_id,
    )
    
    