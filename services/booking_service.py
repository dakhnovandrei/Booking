from UOW import UnitOfWork
from schemas.booking_schemas import BookingCreate


class BookingService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def create_booking(self, user_id: int, data: BookingCreate):
        pass
