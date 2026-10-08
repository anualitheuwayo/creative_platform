import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.models.artwork_model import Artwork
from app.models.user_model import User

from app.routers.artist_profile_router import (
    router as artist_profile_router,
)
from app.routers.artwork_router import router as artwork_router
from app.routers.auth_router import router as auth_router
from app.routers.availability_router import (
    router as availability_router,
)
from app.routers.booking_router import (
    router as booking_router,
)
from app.routers.favourite_router import (
    router as favourite_router,
)
from app.routers.notification_router import (
    router as notification_router,
)
from app.routers.user_router import router as user_router

from database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Creative Platform API",
    version="1.0.0",
)


allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("uploads/profile-images", exist_ok=True)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)


app.include_router(user_router)
app.include_router(artwork_router)
app.include_router(auth_router)
app.include_router(artist_profile_router)
app.include_router(favourite_router)
app.include_router(availability_router)
app.include_router(booking_router)
app.include_router(notification_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to the Creative Platform API",
    }