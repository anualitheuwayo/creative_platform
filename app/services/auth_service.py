from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import (
    create_access_token,
    verify_password,
)
from app.repositories import user_repository


def login_user(
    db: Session,
    email: str,
    password: str,
) -> dict:
    user = user_repository.get_user_by_email(
        db=db,
        email=email,
    )

    invalid_credentials = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    if not user:
        raise invalid_credentials

    if not verify_password(
        password,
        user.password_hash,
    ):
        raise invalid_credentials

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    access_token = create_access_token(
        data={
            "sub": str(user.user_id),
            "role": user.role.value,
        }
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }