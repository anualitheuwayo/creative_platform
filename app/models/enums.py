from enum import Enum


class UserRole(str, Enum):
    CLIENT = "client"
    ARTIST = "artist" 