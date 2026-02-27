from models import Room, User
from repositories.room_repo import RoomRepo
from schemas.exception_schemas import InvalidUserType
from schemas.room_schemas import RoomCreate
from services.user_service import UserService


class RoomService:
    def __init__(self, room_repo: RoomRepo):
        self.room_repo = room_repo

    async def create_room(self, user: User, room_data: RoomCreate) -> Room:
        if user.user_type != 'owner':
            raise InvalidUserType('Вы не можете создавать объявления')
        room = self.room_repo.create_room(user_id=user.id, **room_data.model_dump())
        #Создавать тут записи в календаре доступных объявлений!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        return room
