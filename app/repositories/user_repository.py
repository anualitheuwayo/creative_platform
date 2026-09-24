from typing import Optional

from sqlalchemy.orm import Session

from app.models.user_model import User
from app.models.enums import UserRole


def create_user(
    db: Session,
    full_name: str,
    email: str,
    password_hash: str,
    role: UserRole,
) -> User:
    user = User(
        full_name=full_name,
        email=email,
        password_hash=password_hash,
        role=role,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_id(
    db: Session,
    user_id: int,
) -> Optional[User]:
    return (
        db.query(User)
        .filter(User.user_id == user_id)
        .first()
    )


def get_user_by_email(
    db: Session,
    email: str,
) -> Optional[User]:
    return (
        db.query(User)
        .filter(User.email == email)
        .first()
    )


def get_users(
    db: Session,
    skip: int = 0,
    limit: int = 100,
) -> list[User]:
    return (
        db.query(User)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_user(
    db: Session,
    user: User,
    update_data: dict,
) -> User:
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)

    return user


def delete_user(
    db: Session,
    user: User,
) -> None:
    db.delete(user)
    db.commit()