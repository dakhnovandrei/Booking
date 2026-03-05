from datetime import date, timedelta

from models import Room, User, AvailabilityCalendar
from repositories.availabilitycalendar_repo import AvailabilityCalendarRepo
from repositories.room_repo import RoomRepo
from schemas.exception_schemas import InvalidUserType
from schemas.room_schemas import RoomCreate
from services.user_service import UserService


class RoomService:
    def __init__(self, room_repo: RoomRepo, calendar_repo: AvailabilityCalendarRepo):
        self.room_repo = room_repo
        self.calendar_repo = calendar_repo

    async def create_room(self, user: User, room_data: RoomCreate) -> Room:
        if user.user_type == 'guest':
            raise InvalidUserType('Вы не можете создавать объявления')

        room = self.room_repo.create_room(user.id, **room_data.model_dump())
        await self.calendar_repo.create_calendar(room.id)

        return room
