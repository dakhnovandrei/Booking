from datetime import date, timedelta
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
                is_checked_out=True
            )
            dates.append(calendar_date)
        self.session.add_all(dates)
        await self.session.flush()

    async def get_dates_range(self, room_id: int, start_date: date, end_date: date):
        stmt = select(self.model).where(self.model.property_id == room_id).where(
            between(self.model.date, start_date, end_date)).where(self.model.is_available.is_(True))
        results = self.session.execute(stmt)
        return results.scalar.all()

    async def block_dates(self, room_id: int, start_date: date, end_date: date):
        dates = update(self.model).where(self.model.property_id == room_id).where(
            between(self.model.date, start_date, end_date)).values(
            is_available=False, is_blocked=True)
        await self.session.execute(dates)
        await self.session.flush()
