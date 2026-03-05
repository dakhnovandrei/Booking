from datetime import date, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

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
