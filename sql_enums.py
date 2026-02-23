import enum


class UserType(str, enum.Enum):
    GUEST = 'guest'
    OWNER = 'owner'
    OWNER_GUEST = 'owner_guest'


class BookingStatus(str, enum.Enum):
    CREATED = 'created'
    REJECTED = 'rejected'
    CONFIRMED = "confirmed"


class RoomStatus(str, enum.Enum):
    ACTIVE = "active"
    HIDDEN = "hidden"
    BLOCKED = "blocked"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
