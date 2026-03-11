from datetime import date, timedelta

from models import Room, User, AvailabilityCalendar
from repositories.availabilitycalendar_repo import AvailabilityCalendarRepo
from repositories.room_repo import RoomRepo
from schemas.exception_schemas import InvalidUserType, RoomNotFound
from schemas.room_schemas import RoomCreate, RoomSearchParams, RoomUpdate
from services.user_service import UserService


class RoomService:
    def __init__(self, room_repo: RoomRepo, calendar_repo: AvailabilityCalendarRepo):
        self.room_repo = room_repo
        self.calendar_repo = calendar_repo

    async def create_room(self, user: User, room_data: RoomCreate) -> Room:
        if user.user_type == 'guest':
            raise InvalidUserType('Вы не можете создавать объявления')

        room = await self.room_repo.create_room(user.id, **room_data.model_dump())
        await self.calendar_repo.create_calendar(room.id)

        return room

    async def get_room_by_id(self, room_id: int):
        room = await self.room_repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFound(f"Комнаты с id: {room_id} не существует")

        return room

    async def search_room(self, room_params: RoomSearchParams):
        return await self.room_repo.listing_room(room_params)

    async def update_room(self, room_id: int, user: User, data: RoomUpdate):
        room = await self.room_repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFound(f"Комнаты не существует")
        if user.user_type == 'guest':
            raise InvalidUserType("Пользователь не имеет права сдавать жилье в аренду")

        await self.room_repo.update_room_info(room, data)

    async def delete_room(self, room_id: int, owner: User):
        room = await self.room_repo.get_room_by_id(room_id)
        if not room:
            raise RoomNotFound("Комната не найдена")
        if owner.user_type == 'guest':
            raise InvalidUserType("Данный пользователь не может удалить комнату")

        await self.room_repo.delete_room(room_id)
