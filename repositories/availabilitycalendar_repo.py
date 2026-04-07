from datetime import datetime, timedelta
from sqlalchemy import select, update, between
from models import AvailabilityCalendar, Room


class AvailabilityCalendarRepo:
    model = AvailabilityCalendar

    def __init__(self, session):
        self.session = session

    async def create_calendar(self, room: Room):
        today = date.today()
        days_forward = 365
        dates = []
        for i in range(days_forward):
            current_date = today + timedelta(days=i)

            calendar_date = AvailabilityCalendar(
                property_id=room.id,
                date=current_date,
                price=room.base_price,
                is_available=True,
                is_blocked=False,
                is_checked_out=False
            )
            dates.append(calendar_date)
        self.session.add_all(dates)
        await self.session.flush()

    async def get_dates_range(self, room_id: int, start_date: datetime, end_date:datetime):
        stmt = select(self.model).where(self.model.property_id == room_id).where(
            between(self.model.date, start_date, end_date)).where(self.model.is_available.is_(True))
        results = await self.session.execute(stmt)
        await self.session.flush()
        return results.scalars().all()

    async def release_booking_dates(self, booking_id: int):
        stmt = update(self.model).where(self.model.booking_id == booking_id).values(booking_id=None, is_available=True)
        await self.session.execute(stmt)
        await self.session.flush()

    async def block_dates(self, room_id: int, start_date: datetime, end_date: datetime):
        dates = update(self.model).where(self.model.property_id == room_id).where(
            between(self.model.date, start_date, end_date)).values(
            is_available=False, is_blocked=True)
        await self.session.execute(dates)
        await self.session.flush()

    async def release_blocked_dates(self, room_id: int, start_date:datetime, end_date:datetime):
        stmt = update(self.model).where(self.model.property_id == room_id).where(
            self.model.date.between(start_date, end_date)).values(
            is_available=True, is_blocked=False
        )
        await self.session.execute(stmt)
        await self.session.flush()

    async def update_price_range(self, room_id: int, start_date: datetime, end_date: datetime, price: float):
        dates = update(self.model).where(self.model.property_id == room_id).where(
            between(self.model.date, start_date, end_date)).values(
            price=price
        )
        await self.session.execute(dates)
        await self.session.flush()

    async def get_dates_for_update(self, room_id: int, start_date: datetime, end_date:datetime):
        stmt = select(self.model).where(self.model.property_id == room_id).where(
            self.model.date.between(start_date, end_date)).with_for_update()
        res_dates = await self.session.execute(stmt)
        await self.session.flush()
        return res_dates.scalars().all()

    async def set_booking(self, room_id: int, start_date: datetime, end_date: datetime, booking_id: int):
        stmt = update(self.model).where(self.model.property_id == room_id).where(self.model.date.between(
            start_date, end_date)).values(is_available=False, booking_id=booking_id)
        await self.session.execute(stmt)
        await self.session.flush()
