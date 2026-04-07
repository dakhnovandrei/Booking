from typing import List

from select import select
from sqlalchemy import insert, update

from models import Booking
from schemas.booking_schemas import BookingCreate


class BookingRepo:
    model = Booking

    def __init__(self, session):
        self.session = session

    async def create_booking(self, data: BookingCreate) -> model:
        booking_data = data.model_dump()
        new_instance = self.model(**booking_data)
        self.session.add(new_instance)
        await self.session.flush()
        return new_instance

    async def get_booking_by_id(self, booking_id: int) -> model:
        booking = await self.session.execute(select(self.model).where(self.model.id == booking_id))
        return booking.scalar_or_none()

    async def get_user_bookings(self, user_id: int) -> List[model] | model:
        bookings = await self.session.execute(
            select(self.model).where(self.model.guest_id == user_id)
        )
        return bookings.scalars().all()

    async def cancel_booking(self, booking_id: int):
        stmt = update(self.model).where(self.model.id == booking_id).values(
            is_canceled=True
        )
        await self.session.execute(stmt)
        await self.session.flush()

    async def get_booking_for_update(self, booking_id: int) -> model:
        stmt = select(self.model).where(self.model.id == booking_id).with_for_update()
        booking = await self.session.execute(stmt)
        return booking.scalar_or_none()
