import jwt

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.core.security import ALGORITHM, SECRET_KEY
from app.models.enums import UserRole
from app.models.user_model import User
from database import get_db


bearer_scheme = HTTPBearer()


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials.",
    headers={
        "WWW-Authenticate": "Bearer",
    },
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(
        bearer_scheme
    ),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM],
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (
        jwt.PyJWTError,
        ValueError,
        TypeError,
    ):
        raise credentials_exception

    user = db.query(User).filter(
        User.user_id == user_id
    ).first()

    if not user:
        raise credentials_exception

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user.",
        )

    return user


def require_artist(
    current_user: User = Depends(get_current_user),
) -> User:
    if current_user.role != UserRole.ARTIST:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only artists can perform this action.",
        )

    return current_user