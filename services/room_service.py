from datetime import date, timedelta

from UOW import UnitOfWork
from models import Room, User
from schemas.exception_schemas import InvalidUserType, RoomNotFound
from schemas.room_schemas import RoomCreate, RoomSearchParams, RoomUpdate


class RoomService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_room(self, user: User, room_data: RoomCreate) -> Room:
        if user.user_type == 'guest':
            raise InvalidUserType('Вы не можете создавать объявления')
        async with self.uow as uow:
            room = await uow.room.create_room(user.id, room_data)
            await uow.calendar.create_calendar(room)
        return room

    async def get_room_by_id(self, room_id: int):
        async with self.uow as uow:
            room = await uow.room.get_room_by_id(room_id)
        if not room:
            raise RoomNotFound(f"Комнаты с id: {room_id} не существует")

        return room

    async def search_room(self, room_params: RoomSearchParams):
        async with self.uow as uow:
            rooms = await uow.room.listing_room(room_params)
        return rooms

    async def update_room(self, room_id: int, user: User, data: RoomUpdate):
        async with self.uow as uow:
            room = await uow.room.get_room_by_id(room_id)
            if not room:
                raise RoomNotFound(f"Комнаты не существует")
            if user.user_type == 'guest':
                raise InvalidUserType("Пользователь не имеет права сдавать жилье в аренду")

        return await uow.room.update_room_info(room, data)

    async def delete_rooms(self, room_id: int, owner: User):
        async with self.uow as uow:
            room = await uow.room.get_room_by_id(room_id)
            if not room:
                raise RoomNotFound("Комната не найдена")
            if owner.user_type == 'guest':
                raise InvalidUserType("Данный пользователь не может удалить комнату")

            await uow.room.delete_room(room_id)
