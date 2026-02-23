from sqlalchemy import select, delete
from schemas.user_schemas import UserRegister, UserUpdate
from models import User


class UserRepo:
    model = User

    def __init__(self, session):
        self.session = session

    async def create_user(self, user_data: UserRegister) -> User:
        new_instance = self.model(**user_data.model_dump())
        self.session.add(new_instance)
        await self.session.flush()
        return new_instance

    async def get_user_by_email(self, email: str) -> User | None:
        user = await self.session.execute(
            select(self.model).where(self.model.email == email)
        )
        return user.scalar_one_or_none()

    async def get_user_by_id(self, us_id: int) -> User | None:
        user = await self.session.execute(
            select(self.model).where(self.model.id == us_id)
        )
        return user.scalar_one_or_none()

    async def get_user_by_phone(self, phone: str) -> User | None:
        user = await self.session.execute(
            select(self.model).where(self.model.phone == phone)
        )
        return user.scalar_one_or_none()

    async def update(self, user: User, data: UserUpdate) -> User:
        updated_data = data.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(user, key, value)
        await self.session.flush()
        return user

    async def delete_user(self, user: User) -> None:
        await self.session.delete(user)
        await self.session.flush()
