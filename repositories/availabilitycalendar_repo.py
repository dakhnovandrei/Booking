from sqlalchemy.ext.asyncio import AsyncSession


class AvailabilityCalendarRepo:
    def __init__(self, session):
        self.session = session


    async def create_calendar(self, ):
        pass