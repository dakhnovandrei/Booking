from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum
from database import Base
import enum

class UserType(str, enum.Enum):
    GUEST = 'guest'
    OWNER = 'owner'
    OWNER_GUEST = 'owner_guest'




class User(Base):
    first_name: Mapped[str]
    second_name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[str | None]
    user_type: Mapped[UserType] = mapped_column(Enum(UserType))
    is_verified: Mapped[bool]
    verification_lvl: Mapped[int] = mapped_column(default=0)
    booking_cnt: Mapped[int] = mapped_column(default=0)
    listings_list: Mapped[int] = mapped_column(default=0)