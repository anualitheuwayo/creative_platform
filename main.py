from fastapi import FastAPI
import os

from fastapi.staticfiles import StaticFiles
from app.models.user_model import User
from app.routers.user_router import router as user_router
from app.models.artwork_model import Artwork
from app.routers.artwork_router import router as artwork_router
from app.routers.auth_router import router as auth_router
from app.routers.artist_profile_router import (
    router as artist_profile_router,
)
from database import Base, engine


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Creative Marketplace API",
)

os.makedirs(
    "uploads/profile-images",
    exist_ok=True,
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

app.include_router(user_router)
app.include_router(artwork_router)
app.include_router(auth_router)
app.include_router(artist_profile_router)
@app.get("/")
def home():
    return {
        "message": "Welcome to the Creative Marketplace API"
    }