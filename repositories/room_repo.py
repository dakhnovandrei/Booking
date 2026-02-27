from sqlalchemy import select, delete, func
from models import Room, AvailabilityCalendar
from schemas.room_schemas import RoomCreate, RoomUpdate, RoomSearchParams
from sql_enums import RoomStatus


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
            select(self.model).where(self.model.id == room_id)
        )
        return room.scalar_one_or_none()

    async def update_room_info(self, room: model, room_data: RoomUpdate) -> model:
        updated_data = room_data.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(room, key, value)
        await self.session.commit()
        await self.session.refresh(room)
        return room

    async def listing_room(self, filters: RoomSearchParams) -> list[model]:
        stmt = select(self.model).where(self.model.status == RoomStatus.ACTIVE)
        if filters.country:
            stmt = stmt.where(self.model.country == filters.country)
        if filters.city:
            stmt = stmt.where(self.model.city == filters.city)
        if filters.guests:
            stmt = stmt.where(self.model.guests_cnt >= filters.guests)
        if filters.min_price:
            stmt = stmt.where(self.model.base_price >= filters.min_price)
        if filters.max_price:
            stmt = stmt.where(self.model.base_price <= filters.max_price)
        if filters.check_in and filters.check_out:
            days_count = (filters.check_out - filters.check_in).days
            availability_subquery = (
                select(AvailabilityCalendar.property_id).where(
                    AvailabilityCalendar.date >= filters.check_in,
                    AvailabilityCalendar.date < filters.check_out,
                    AvailabilityCalendar.is_available == True,
                    AvailabilityCalendar.booking_id.is_(None)
                )
                .group_by(AvailabilityCalendar.property_id)
                .having(func.count() == days_count)
                .subquery()
            )
            stmt = stmt.where(Room.id.in_(availability_subquery))

        offset = (filters.page - 1) * filters.page_size
        stmt = stmt.offset(offset).limit(filters.page_size)

        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def delete_room(self, room_id: int):
        await self.session.execute(
            delete(self.model).where(self.model.id == room_id)
        )
        await self.session.commit()
