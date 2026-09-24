from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.auth_schema import (
    LoginRequest,
    TokenResponse,
)
from app.services.auth_service import login_user
from database import get_db


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db),
):
    return login_user(
        db=db,
        email=login_data.email,
        password=login_data.password,
    )