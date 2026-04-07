from core.database import get_session, async_session_maker
from repositories.availabilitycalendar_repo import AvailabilityCalendarRepo
from repositories.room_repo import RoomRepo
from repositories.user_repo import UserRepo
from repositories.booking_repo import BookingRepo


class UnitOfWork:
    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def __aenter__(self):
        self.session = self._session_factory()
        self.calendar = AvailabilityCalendarRepo(self.session)
        self.user = UserRepo(self.session)
        self.room = RoomRepo(self.session)
        self.booking = BookingRepo(self.session)

        return self

    async def __aexit__(self, exc_type, *args):
        if exc_type:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()


async def get_uow():
    async with UnitOfWork(async_session_maker) as uow:
        yield uow
