from datetime import datetime
import datetime as dt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Enum, Index, Numeric, String
from core.database import Base
from sql_enums import PaymentStatus, UserType, BookingStatus, RoomStatus, RoomType, Currency
from decimal import Decimal


class User(Base):
    first_name: Mapped[str]
    second_name: Mapped[str]
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    phone: Mapped[str | None] = mapped_column(unique=True, index=True)
    user_type: Mapped[UserType] = mapped_column(Enum(UserType), index=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    verification_lvl: Mapped[int] = mapped_column(default=0)
    guest_bookings: Mapped[list["Booking"]] = relationship(
        back_populates='guest',
        foreign_keys='Booking.guest_id'
    )

    cancelled_bookings: Mapped[list["Booking"]] = relationship(
        back_populates='cancelled_by_user',
        foreign_keys='Booking.cancelled_by'
    )


class Room(Base):
    owner_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'), index=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[str] = mapped_column(String(1000))

    country: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(250))

    property_type: Mapped[RoomType] = mapped_column(Enum(RoomType), index=True)

    guests_cnt: Mapped[int]
    bedrooms: Mapped[int]
    beds: Mapped[int]
    bathrooms: Mapped[int]

    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    currency: Mapped[Currency] = mapped_column(Enum(Currency))
    cleaning_fee: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    security_deposit: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    weekend_multiplier: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    min_stay: Mapped[int]
    max_stay: Mapped[int]

    is_available: Mapped[bool] = mapped_column(default=True, index=True)
    status: Mapped[RoomStatus] = mapped_column(Enum(RoomStatus), index=True, default=RoomStatus.ACTIVE)
    last_booked_at: Mapped[datetime | None] = mapped_column(index=True)

    bookings: Mapped[list["Booking"]] = relationship(back_populates="property")
    availability: Mapped[list["AvailabilityCalendar"]] = relationship(back_populates="room")


class Booking(Base):
    booking_number: Mapped[int] = mapped_column(unique=True, index=True)
    property_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'), index=True)
    guest_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    guest_cnt: Mapped[int]

    status: Mapped[BookingStatus] = mapped_column(Enum(BookingStatus), default=BookingStatus.CREATED, index=True)

    check_in: Mapped[datetime]
    check_out: Mapped[datetime]

    price_per_night: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2))

    currency: Mapped[str]

    payment_status: Mapped[PaymentStatus] = mapped_column(Enum(PaymentStatus), default=PaymentStatus.PENDING,
                                                          index=True)
    cancelled: Mapped[bool] = mapped_column(default=False)

    cancelled_by: Mapped[int | None] = mapped_column(ForeignKey('users.id'), nullable=True)

    expires_at: Mapped[datetime]

    guest: Mapped["User"] = relationship(
        back_populates="guest_bookings",
        foreign_keys=[guest_id]
    )

    cancelled_by_user: Mapped["User"] = relationship(
        back_populates="cancelled_bookings",
        foreign_keys=[cancelled_by]
    )
    property: Mapped[list["Room"]] = relationship(back_populates='bookings')
    dates: Mapped[list["AvailabilityCalendar"]] = relationship(back_populates="booking")


class AvailabilityCalendar(Base):
    property_id: Mapped[int] = mapped_column(ForeignKey('rooms.id', ondelete='CASCADE'), index=True)
    date: Mapped[dt.date] = mapped_column(index=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    booking_id: Mapped[int | None] = mapped_column(ForeignKey('bookings.id'), nullable=True)
    is_available: Mapped[bool] = mapped_column(default=True)
    is_blocked: Mapped[bool] = mapped_column(default=False)
    is_checked_out: Mapped[bool] = mapped_column(default=True)
    room: Mapped["Room"] = relationship(back_populates="availability")
    booking: Mapped["Booking"] = relationship(back_populates="dates")


Index(
    'ix_unique_room_date',
    AvailabilityCalendar.property_id,
    AvailabilityCalendar.date,
    unique=True
)
