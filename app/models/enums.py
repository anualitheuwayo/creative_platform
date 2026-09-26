from enum import Enum


class UserRole(str, Enum):
    ARTIST = "artist"
    CLIENT = "client"


class BookingStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class NotificationType(str, Enum):
    BOOKING_CREATED = "booking_created"
    BOOKING_ACCEPTED = "booking_accepted"
    BOOKING_REJECTED = "booking_rejected"
    BOOKING_CANCELLED = "booking_cancelled"
    ARTWORK_FAVOURITED = "artwork_favourited"
    SYSTEM = "system"