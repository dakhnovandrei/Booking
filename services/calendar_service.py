from datetime import date

from UOW import UnitOfWork
from models import Room
from schemas.exception_schemas import DatesNotFound, DatesBlockError


class AvailabilityCalendarService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def generate_calendar(self, room: Room):
        async with self.uow as uow:
            await uow.calendar.create_calendar(room)

    async def check_availability(self, room_id: int, start_date: date, end_date: date):
        async with self.uow as uow:
            dates = uow.calendar.get_dates_range(room_id, start_date, end_date)
        if not dates:
            raise DatesNotFound("На данное жилье не было найдено свободных дат")
        return dates

    async def block_dates_by_owner(self, room_id: int, start_date: date, end_date: date):
        async with self.uow as uow:
            dates = uow.calendar.block_dates(room_id, start_date, end_date)
        if not dates:
            raise DatesBlockError('Ошибка при блокировке дат')

    async def update_price(self, room_id: int, start_date: date, end_date: date):
        async with self.uow as uow:
            dates_prices = uow.calendar.update_price_range(room_id, start_date, end_date)
        if not dates_prices:
            raise DatesNotFound('Ошибка при изменении цены')
