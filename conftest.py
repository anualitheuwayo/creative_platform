import os

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from datetime import date, time, timedelta
from app.core.security import create_access_token
from app.models.artist_profile_model import ArtistProfile
from app.models.artwork_model import Artwork
from app.models.enums import (
    BookingStatus,
    NotificationType,
    UserRole,
)
from app.models.favourite_model import Favourite
from app.models.user_model import User
from app.models.availability_model import Availability
from app.models.booking_model import Booking
from app.models.notification_model import Notification
from database import Base, get_db
from main import app


load_dotenv()


TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


if not TEST_DATABASE_URL:
    raise ValueError(
        "TEST_DATABASE_URL is missing. Add it to the .env file."
    )


test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)


TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=test_engine,
)


@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture()
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = TestingSessionLocal(
        bind=connection,
    )

    yield session

    session.close()

    if transaction.is_active:
        transaction.rollback()

    connection.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    try:
        with TestClient(app) as test_client:
            yield test_client
    finally:
        app.dependency_overrides.clear()


@pytest.fixture()
def artist_user(db_session):
    user = User(
        full_name="Test Artist",
        email="artist@example.com",
        password_hash="hashed_password",
        role=UserRole.ARTIST,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture()
def client_user(db_session):
    user = User(
        full_name="Test Client",
        email="client@example.com",
        password_hash="hashed_password",
        role=UserRole.CLIENT,
        is_active=True,
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture()
def artist_token_headers(artist_user):
    access_token = create_access_token(
        data={
            "sub": str(artist_user.user_id),
        }
    )

    return {
        "Authorization": f"Bearer {access_token}",
    }


@pytest.fixture()
def client_token_headers(client_user):
    access_token = create_access_token(
        data={
            "sub": str(client_user.user_id),
        }
    )

    return {
        "Authorization": f"Bearer {access_token}",
    }


@pytest.fixture()
def artist_profile(db_session, artist_user):
    profile = ArtistProfile(
        artist_id=artist_user.user_id,
        bio="Test artist profile.",
        specialization="Digital Art",
        location="Nairobi",
        hourly_rate=100.00,
        is_verified=False,
    )

    db_session.add(profile)
    db_session.commit()
    db_session.refresh(profile)

    return profile


@pytest.fixture()
def artwork(
    db_session,
    artist_user,
    artist_profile,
):
    new_artwork = Artwork(
        artist_id=artist_user.user_id,
        title="Test Artwork",
        description="Artwork created for favourite endpoint tests.",
        price=100.00,
        image_url="https://example.com/test-artwork.jpg",
        category="Digital Art",
        is_available=True,
    )

    db_session.add(new_artwork)
    db_session.commit()
    db_session.refresh(new_artwork)

    return new_artwork


@pytest.fixture()
def favourite(
    db_session,
    client_user,
    artwork,
):
    new_favourite = Favourite(
        client_id=client_user.user_id,
        artwork_id=artwork.artwork_id,
    )

    db_session.add(new_favourite)
    db_session.commit()
    db_session.refresh(new_favourite)

    return new_favourite

@pytest.fixture()
def availability(
    db_session,
    artist_user,
):
    slot = Availability(
        artist_id=artist_user.user_id,
        available_date=date.today() + timedelta(days=7),
        start_time=time(9, 0),
        end_time=time(12, 0),
        is_available=True,
    )

    db_session.add(slot)
    db_session.commit()
    db_session.refresh(slot)

    return slot

@pytest.fixture()
def booking(
    db_session,
    client_user,
    availability,
):
    new_booking = Booking(
        client_id=client_user.user_id,
        artist_id=availability.artist_id,
        availability_id=availability.availability_id,
        message="Test booking message.",
        status=BookingStatus.PENDING,
    )

    availability.is_available = False

    db_session.add(new_booking)
    db_session.commit()
    db_session.refresh(new_booking)

    return new_booking

@pytest.fixture()
def notification(
    db_session,
    client_user,
):
    new_notification = Notification(
        recipient_id=client_user.user_id,
        notification_type=NotificationType.SYSTEM,
        message="Test notification message.",
        is_read=False,
    )

    db_session.add(new_notification)
    db_session.commit()
    db_session.refresh(new_notification)

    return new_notification