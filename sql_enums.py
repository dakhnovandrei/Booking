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


class RoomType(str, enum.Enum):
    STUDIO = 'studio'
    ONE_ROOM = 'one_room'
    TWO_ROOMS = 'two_room'
    THREE_ROOMS = 'three_rooms'
    FOUR_PLUS_ROOMS = 'four_plus_rooms'
    APARTMENT = 'apartment'
    SERVICED_APARTMENT = 'serviced_apartment'
    HOUSE = 'house'
    TOWNHOUSE = 'townhouse'
    ROOM = 'room'
    LOFT = 'loft'


class Currency(str, enum.Enum):
    EUR = "EUR"
    USD = "USD"
    RUB = "RUB"


class PaymentStatus(str, enum.Enum):
    PENDING = "pending"
    PAID = "paid"
    FAILED = "failed"
