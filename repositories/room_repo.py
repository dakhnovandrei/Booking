from sqlalchemy import select, delete
from models import Room
from schemas.room_schemas import RoomCreate, RoomUpdate


class RoomRepo:
    model = Room

    def __init__(self, session):
        self.session = session

    async def create_room(self, user_id: int, room_data: RoomCreate) -> model:
        new_instance = self.model(owner_id=user_id, **room_data.model_dump())
        self.session.add(new_instance)
        await self.session.commit()
        await self.session.refresh(new_instance)
        return new_instance

    async def get_room_by_id(self, room_id: int) -> model:
        room = self.session.execute(
            select(Room).where(Room.id == room_id)
        )
        return room.scalar_one_or_none()

    async def update_room_info(self, room_id: int, room_data: RoomUpdate):
        pass

    async def delete_room(self, room_id: int):
        await self.session.execute(
            delete(Room).where(Room.id == room_id)
        )
        await self.session.commit()
